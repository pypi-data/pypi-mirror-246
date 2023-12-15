"""
# this routine reads the AVM upload methods (env and mesh) and
# produces the equivalent TR181 structure to be used by the AXWIFI core
#
# for data structure conversion check https://wiki.axiros.com/pages/viewpage.action?spaceKey=AXWIFI&title=Data+vs+TR181
# for data structure check https://wiki.axiros.com/display/AXWIFI/AVM+Upload+methods#AVMUploadmethods-AVMWiFiMeshonDemo
"""
from devapp.app import app
from operators.core import ax_core_ops
from netaddr import EUI
from operators.con import con
import time

ax = ax_core_ops
now = time.time


def node_tmpl(n):
    return {
        'PhysAddress': str(EUI(n['device_mac_address'])),
        'Manufacturer': n['device_manufacturer'],
        'SoftwareVersion': n['device_firmware_version'],
        'HostName': n['device_name'],
        'ModelName': n['device_model'],
        'is_meshed': n['is_meshed'],
        'mesh_role': n['mesh_role'],
        'DeviceID': n['uid'],
    }


def wlan_interf_tmpl(wi):
    return {
        'mac_address': str(EUI(wi['mac_address'])),
        'channel_utilization': wi.get('channel_untilization'),
        'current_channel': wi.get('current_channel', 0),
        'op_mode': wi.get('opmode'),
        'phymodes': wi.get('phymodes'),
        'security': wi.get('security'),
        'steering_enabled': wi.get('steering_enabled'),
        'name': wi.get('name'),
        'type': wi.get('type'),
        'node_links': wi.get('node_links'),
    }


def lan_interf_tmpl(li):
    return {
        'mac_address': str(EUI(li['mac_address'])),
        'name': li.get('name'),
        'type': li.get('type'),
        'node_links': li.get('node_links'),
    }


def link_tmpl(n):
    return {
        'cur_data_rate_rx': n.get('cur_data_rate_rx', 0),
        'cur_data_rate_tx': n.get('cur_data_rate_tx', 0),
        'last_connected': n.get('last_connected', 0),
        'node_1_uid': n.get('node_1_uid', 'n-1'),
        'node_2_uid': n.get('node_2_uid', 'n-1'),
        'type': n.get('type', 'LAN'),
        'rssi': n.get('rx_rcpi', 0),
    }


def parse_and_merge(data, json_data, method):
    if method == 'env':
        r = env(data, json_data)
    if method == 'mesh':
        r = mesh(data, json_data)
    return r


def mesh(data, j):
    mesh = j['props']['data']
    nodes = {}
    # hierarchy = {'id': 'n-1', 'children': []} # not in use

    for node in mesh['nodes']:
        # exclude nodes with no connected links that are not master or slave
        nodes[node['uid']] = node_tmpl(node)
        nodes[node['uid']]['interfaces'] = []

        i = 1
        for interface in node['node_interfaces']:
            if interface.get('type') == 'LAN':
                ni = lan_interf_tmpl(interface)
                ni['l1interf'] = 'LAN'
                i += 1
            elif interface.get('type') == 'WLAN':
                ni = wlan_interf_tmpl(interface)
                if ni['current_channel'] in range(0, 15):
                    ni['l1interf'] = 'WLAN 2.4GHz'
                elif ni['current_channel'] > 15:
                    ni['l1interf'] = 'WLAN 5GHz'
            else:
                continue

            if interface.get('node_links'):
                connected_links_only = []
                for nl in interface['node_links']:
                    if nl.get('state') != 'CONNECTED':
                        continue
                    node_link = link_tmpl(nl)
                    connected_links_only.append(node_link)
                if connected_links_only:
                    ni['node_links'] = connected_links_only
                    nodes[node['uid']]['interfaces'].append(ni)

        # master shall not be removed even if it has no clients connected
        if not nodes[node['uid']]['interfaces'] and node['uid'] != 'n-1':
            del nodes[node['uid']]

    data['Hosts'] = {'Host': nodes}
    data['metadata']['last_json_mesh_ts'] = j['ts']
    return data


def env(data, j):
    ap_index = 1
    env = j['props']['data']

    tr181_freq_names = {'2.4': '2.4GHz', '5.0': '5GHz'}

    # restructure the noise levels once to be used later
    noises = {}
    noises['2.4'] = {}
    noises['5.0'] = {}
    for noise in env['nf']:
        noises[noise['freqband']][noise['channel']] = noise['noisefloor']

    results = {}
    for ap in env['ap']:
        this_ap = {
            'SSID': ap['ssid'],
            'BSSID': ap['bssid'],
            'SignalStrength': ap['rssi'],
            'Channel': ap['channel'],
            'OperatingFrequencyBand': tr181_freq_names[ap['freqband']],
            'Noise': noises[ap['freqband']].get(ap['channel'], -100),
        }
        results[str(ap_index)] = this_ap
        ap_index += 1

    data['WiFi'].update({'NeighboringWiFiDiagnostic': {'Result': results}})
    data['collector'] = {
        'code': 200,
        'full_scan': 1,
        'light_scan': 0,
        'msg': 'Full Scan',
        'details': 'Updated from AVM JSON file',
    }
    data['metadata']['last_json_wifi_env_ts'] = j['ts']
    return data


def inspect_avm_clients(data):
    if 'last_json_mesh_ts' not in data['metadata']:
        return data

    clients = {}
    for i, host in data['Hosts']['Host'].items():
        if host.get('is_meshed'):
            for interface in host['interfaces']:
                op_mode = interface.get('op_mode')
                if op_mode == 'REPEATER':
                    channel = interface.get('current_channel')
                    if channel:
                        imac = interface.get('mac_address')
                        band = '2' if channel < 14 else '5'
                        name = host.get('HostName') + ' ' + interface.get('name', '')
                        clients[imac] = {'band': band, 'name': name}
                        client_stats = {}
                        node_links = interface.get('node_links')
                        if node_links:
                            nl = node_links[0]
                            client_stats['rssi'] = nl.get('rssi', 0)
                            client_stats['lddr'] = nl.get('cur_data_rate_rx', 0)
                            client_stats['ldur'] = nl.get('cur_data_rate_tx', 0)
                            client_stats['connected_ts'] = nl.get('last_connected', 0)
                        clients[imac].update(client_stats)
        else:
            interface = host['interfaces'][0]
            channel = interface.get('current_channel')
            if channel:
                hmac = host.get('PhysAddress')
                band = '2' if channel < 14 else '5'
                name = host.get('HostName')
                clients[hmac] = {'band': band, 'name': name}
                client_stats = {}
                node_links = interface.get('node_links')
                if node_links:
                    nl = node_links[0]
                    client_stats['rssi'] = nl.get('rssi', 0)
                    client_stats['lddr'] = nl.get('cur_data_rate_rx', 0)
                    client_stats['ldur'] = nl.get('cur_data_rate_tx', 0)
                    client_stats['connected_ts'] = nl.get('last_connected', 0)
                clients[hmac].update(client_stats)

    access_points = data['WiFi'].get('AccessPoint', False)
    if access_points:
        for idx in ('1', '5'):
            mark_for_deletion = []

            for k, v in access_points[idx].get('AssociatedDevice', {}).items():
                # TODO: reevaluate once the hosts and clients status is aligned by AVM
                # if not v.get('Active'):
                #    continue
                mac = v.get('MACAddress')
                if mac in clients:
                    band = clients[mac]['band']
                    if (idx == '1' and band != '2') or (idx == '5' and band != '5'):
                        mark_for_deletion.append(k)
                    else:
                        v['HostName'] = clients[mac]['name']
                        v['SignalStrength'] = clients[mac]['rssi']
                        v['LastDataDownlinkRate'] = clients[mac]['lddr']
                        v['LastDataUplinkRate'] = clients[mac]['ldur']
                        v['AssociationTime'] = clients[mac]['connected_ts']
                        # TODO: reevaluate once the hosts and clients status is aligned by AVM
                        v['Active'] = 1

            for entry in mark_for_deletion:
                del access_points[idx]['AssociatedDevice'][entry]

    return data


class Operators:
    inspect_avm_clients = inspect_avm_clients
