#!/usr/bin/env python
# fmt:off
import time
from types import SimpleNamespace
from collections import Counter
import statistics
from devapp.app import app
from operators.core import ax_core_ops
from operator import itemgetter
from ax.utils.ax_tree import AXTree
from wifi.vendors.vendors import vendors
from wifi.core.delta_q import detect_extender

ax = ax_core_ops

# PME
# Supported Ops
OPS = ['ratio', 'diff', 'drop', 'avg']
RELATIONS = ['higher', 'lower', 'equal', 'N/A']

now = time.time

def merge_array_configs(original_config, new_configs):
    """
    gets the original_config in the form of [{'name': 'foo', 'valu1': ...}, {'name': 'bar', 'value1': ...}]
    and the new_configs in the form an array of the above ( [[{'name':..., ...}, ..], [], ...])
    and overrides the new_configs one by one over the original_config
    """
    names = {}
    for i in range(len(original_config)):
        names[original_config[i]['name']] = i
    for new_config in new_configs:
        for conf in new_config:
            if conf['name'] in names:
                original_config[names[conf['name']]] = conf
    return original_config


def merge_dict_configs(original_config, new_configs):
    """
    get the original configs in the form of {'foo': {}, 'bar': {}, ...}
    and the new_configs in the form an array from above [{'foor: {}, ...}, {....}]
    and overrides the new_configs one by one over the original_config
    """
    for new_config in new_configs:
        for name, value in new_config.items():
            original_config[name] = value
    return original_config


def identify_associateddevices(data, **kw):
    """
    Identify the type of each associated devices (Client, Extender, Mesh)
    """
    def _is_mesh_device(mac, hosts):
        for host in hosts.values():
            if host['PhysAddress'] == mac:
                if {host.get('vendor', 'all'): host.get('ModelName', 'all')} in MeshModels:
                    return True
        return False

    MeshModels = kw.get('mesh_models', [])

    for this_band in data['to_band'].keys():
        if 'clients' not in data['to_band'][this_band].keys():
            data['to_band'][this_band]['clients'] = {}
        extender_count = 0
        mesh_count = 0
        BSSIDs = {}
        for ssid_index, this_ssid in data['to_band'][this_band]['SSID'].items():
            BSSIDs[ssid_index] = this_ssid['BSSID']

        for ssid_index, this_ssid in data['to_band'][this_band]['ssid'].items():
            BSSID = BSSIDs.get(ssid_index, '---')
            for ad in this_ssid.get('clients', {}).get('all', []):
                tp = 'Client'
                this_mac = ad.get('MACAddress', '')
                if 'Type' in ad:
                    tp = ad['Type']
                elif detect_extender(BSSID, this_mac):
                    tp = 'Extender'
                    if _is_mesh_device(this_mac, data.get('Hosts', {'Hosts': {}})['Hosts']):
                        tp = 'Mesh'
                if tp in ('Repeater', 'Mesh'):
                    mesh_count += 1
                elif tp == 'Extender':
                     extender_count += 1

                ad['Type'] = tp
        data['to_band'][this_band]['clients']['mesh_count'] = mesh_count
        data['to_band'][this_band]['clients']['extender_count'] = extender_count

    return data

def identify_changes(data):
    """
    Identify change owners based on current and previous readings

    Owners may be:
    - auto channel: when auto channel is enabled and there was a change
    - axwifi: when the current channel is equal to the last enforced channel
    - manual: if there was a change, but it wasn't performed by auto channel nor by axwifi
    """
    hist = data.get('history', {}).get('events')
    if not hist:
        return data

    last_evt = data['history']['events'][0][1]
    data['cache'] = last_evt.get('cache', {})

    def tmpl():
        return {
            'auto': 0,
            'axwifi': 0,
            'manual': 0,
            'owner': None,
            'ts': 0
        }

    for b, i in data['WiFi']['RadioRefs'].items():
        if not i:
            app.debug('Band not active', band=b)
            continue
        changes = last_evt[b].get('changes', {})
        last_ch = last_evt['WiFi']['Radio'][i]['Channel']
        cur_ch = data['WiFi']['Radio'][i]['Channel']
        autoch_status = data['WiFi']['Radio'][i]['AutoChannelEnable']
        enf_ch = None
        ts = data['ts']
        band_cache = data['cache'].get(b)
        if band_cache:
            enf_ch = band_cache.get('last_enf_ch')
            enf_ts = band_cache.get('last_enf_ts')
            data['cache'][b]['dt_last_enf'] = now() - enf_ts

        b_data = data['to_band'][b]
        d = tmpl()

        if not last_ch or cur_ch == last_ch:
            d['owner'] = changes.get('owner', '')
            d['ts'] = changes.get('ts', -1)
        elif autoch_status:
            d['auto'] = 1
            d['owner'] = 'auto'
            d['ts'] = ts
        elif cur_ch == enf_ch:
            d['axwifi'] = 1
            d['owner'] = 'axwifi'
            d['ts'] = enf_ts
        else:
            d['manual'] = 1
            d['owner'] = 'manual'
            d['ts'] = ts

        b_data['changes'] = d
        app.debug('Change analysis', details=d)
    return data


def inspect_hosts(data):
    """
    Enrich WLAN Hosts data with AssociatedDevices data and vice-versa
    """

    if not data.get('Hosts'):
        return

    hosts = data['Hosts']['Host']
    ssids = data['WiFi']['SSID']

    data['tmp'] = tmp = {'hosts_macs': []}
    hosts_by_mac = {}
    for i, host in hosts.items():
        if host.get('Active', 1) == 0:
            continue
        if host.get('PhysAddress'):
            mac = host['PhysAddress']
            host['vendor'] = vendor(mac)
            hosts_by_mac[mac] = host
            hosts_by_mac[mac]['hindex'] = i
            tmp['hosts_macs'].append(host['PhysAddress'])

    for idx, ssid in ssids.items():
        band = ssid['band']
        if ssid.get('AssociatedDevice'):
            for i, ad in ssid['AssociatedDevice'].items():
                mac = ad.get('MACAddress')
                ss = ad.get('SignalStrength', 0)
                lddr = ad.get('LastDataDownlinkRate', 0)
                ldur = ad.get('LastDataUplinkRate', 0)
                ip = ad.get('IPAddress')
                if not mac:
                    continue
                if mac not in tmp['hosts_macs']:
                    tmp['hosts_macs'].append(mac)
                if hosts_by_mac.get(mac):
                    ad['HostName'] = hosts_by_mac[mac].get('HostName', '---')
                    hidx = hosts_by_mac[mac]['hindex']
                    hosts[hidx]['InterfaceType'] = '802.11'
                    if not ip:
                        ad['IPAddress'] = hosts_by_mac[mac].get('IPAddress', '---')
                    if 'LastDataDownlinkRate' not in hosts[hidx]:
                        hosts[hidx]['LastDataDownlinkRate'] = lddr
                    if 'LastDataUplinkRate' not in hosts[hidx]:
                        hosts[hidx]['LastDataUplinkRate'] = ldur
                    if 'SignalStrength' not in hosts[hidx]:
                        hosts[hidx]['SignalStrength'] = ss
                    elif 'SignalStrength' not in ad:
                        ad['SignalStrength'] = hosts[hidx]['SignalStrength']
                    hosts[hidx]['band'] = band
                    #Layer1Interface is mandatory for network map interfaces
                    hosts[hidx]['Layer1Interface'] = 'Device.WiFi.Radio.1' \
                            if band == '2' else 'Device.WiFi.Radio.5'
    return data


def inspect_ieee1905(data):
    try:
        topology = AXTree(data['IEEE1905']['AL']['NetworkTopology'])
        if topology['Status'] != 'Available':
            app.info('IEEE1905 Disabled.')
            return data
    except Exception as e:
        app.info(f'IEEE1905 NetworkTopology not supported: {e}')
        return data

    if not data.get('Hosts'):
        return data
    hosts = {k: v for k, v in data['Hosts']['Host'].items() if v['Active']}

    interfaces_per_dev = {}
    for devk, devv in topology['IEEE1905Device'].items():
        if devv['InterfaceNumberOfEntries'] > 1:
            if devk == '1':
                master_mac = devv['IEEE1905Id']
            interfaces_per_dev[devv['IEEE1905Id']] = [v['InterfaceId'] for v in devv['Interface'].values()]

    for host in hosts.values():
        #if not host.get('Active'):
        #    continue
        ad_pth_split = host['AssociatedDevice'].split('.')
        ad_pth = '.'.join(ad_pth_split[-2:])
        ad = topology[ad_pth]
        ad_idx = ad_pth_split[-1]
        if ad_idx == '1':
            host['DeviceID'] = ad['IEEE1905Id']
            host['Mode'] = 'master'
            continue

        host['DeviceID'] = ad['IEEE1905Id']
        host['vendor'] = ad.get('ManufacturerName')
        host['ModelName'] = ad.get('ManufacturerModel')
        host['Mode'] = 'Repeater' if ad['IEEE1905Id'] in interfaces_per_dev else 'Client'
        num_neighs = ad['IEEE1905NeighborNumberOfEntries']
        if num_neighs:
            idx = 1
            if num_neighs >= 2:
                max_la = 100
                link_availability = 'Metric.1.LinkAvailability'
                for i,j in ad['IEEE1905Neighbor'].items():
                    if j[link_availability] < max_la:
                        max_la = j[link_availability]
                        idx = i

            # retrieve signal strength
            signal = -abs(int(ad[f'IEEE1905Neighbor.{idx}.Metric.1.RSSI']))
            link_avail = ad[f'IEEE1905Neighbor.{idx}.Metric.1.LinkAvailability']
            if signal != -255:
                host['SignalStrength'] = signal
                host['LinkAvailability'] = link_avail
            # retrieve physical rates
            host['LastDataUplinkRate'] = host['LastDataDownlinkRate'] = ad[f'IEEE1905Neighbor.{idx}.Metric.1.PHYRate'] * 1000
            # determine parent node
            neigh_dev_id = ad['IEEE1905Neighbor.1.NeighborDeviceId']
            for k, v in interfaces_per_dev.items():
                if neigh_dev_id in v:
                    if k == master_mac:
                        host['ParentNodeID'] = 'Gateway'
                    else:
                        host['ParentNodeID'] = k
                        host['Mode'] = 'Mesh Client'
                    break
            # determine interface details
            local_interface_idx = 1
            if len(ad['Interface']) > 1:
                local_interface_idx = ad[f'IEEE1905Neighbor.{idx}.LocalInterface'].split('.')[-1]

            host['standard'] = ad[f'Interface.{local_interface_idx}.MediaType']
            band_code = str(ad[f'Interface.{local_interface_idx}.APChannelBand'])
            band_code = int(band_code, 16)
            if band_code == 0:
                host['Layer1Interface'] = 'Device.WiFi.Radio.1'
            elif band_code in (2, 3):
                host['Layer1Interface'] = 'Device.WiFi.Radio.5'
            elif band_code == 255:
                host['Layer1Interface'] = 'LAN'

        if host.get('Mode') != 'master' and 'WiFi' in host['Layer1Interface']:
            _update_ad_table(data, host)

    data['Hosts']['Host'] = hosts
    return data

def _update_ad_table(data, h):
    ad = {
        'MACAddress': h['PhysAddress'],
        'SignalStrength': h['SignalStrength'],
        'OperatingStandard': h['standard'][5:],
        'Active': True,
        'AutenticationState': True,
        'LastDataUplinkRate': h['LastDataUplinkRate'],
        'LastDataDownlinkRate': h['LastDataDownlinkRate'],
        'IPAddress': h['IPAddress'],
        'vendor': h['vendor'],
        'HostName': h['HostName'],
        'Type': h['Mode']
    }

    ap_idx = h['Layer1Interface'][-1]
    band = '2' if ap_idx == '1' else '5'
    ap = data['to_band'][band]['SSID'][ap_idx]
    if 'AssociatedDevice' not in ap:
        ap['AssociatedDevice'] = {}
    ad_idx = str(len(ap['AssociatedDevice'])+1)
    ap['AssociatedDevice'][ad_idx] = ad
    return


def calculate_radio_stats(data):
    """
    Sum up all SSID Stats per Band when Radio Stats are not available
    """
    if not data.get('WiFi') or not data['WiFi'].get('Radio') or not data['WiFi'].get('SSID'):
        return

    radios = data['WiFi']['Radio']
    ssids = data['WiFi']['SSID']

    stats_list = ['BytesSent','BytesReceived','PacketsSent','PacketsReceived','ErrorsSent','ErrorsReceived']

    def stats_tmpl():
        return {'BytesSent': 0, 'BytesReceived': 0, 'PacketsSent': 0, 'PacketsReceived': 0, 'ErrorsSent': 0, 'ErrorsReceived': 0}

    if radios:
        for i, radio in radios.items():
            if radios[i].get('Stats') and stats_list == list(radios[i].get('Stats').keys() & stats_list):
                continue
            else:
                if not data['WiFi']['Radio'][i].get('Stats'):
                    data['WiFi']['Radio'][i]['Stats'] = {}
                data['WiFi']['Radio'][i]['Stats'].update(stats_tmpl())
                for idx, ssid in ssids.items():
                    if 'Stats' not in ssid:
                        continue
                    band = ssids[idx]['band']
                    if (i == '1' and band == '2') or (i == '5' and band == '5'):
                        for key in stats_list:
                            try:
                                data['WiFi']['Radio'][i]['Stats'][key] += ssid['Stats'][key]
                            except Exception as ex:
                                app.error('intel.calculate_radio_stats  | wrong/missing SSID Stats key/val', ex=ex)
                                continue

    return data


def inspect_clients(data):
    """
    Normalize associated devices data
    Analyse RSSI per client
    """
    def stats_tmpl():
        return {'all': [], 'max': 0, 'min': 0, 'mean': 0, 'median': 0, 'stdev': 0}
    def metrics_tmpl():
        return {'lddr': stats_tmpl(), 'ldur': stats_tmpl(), 'esent': stats_tmpl(), 'erec': stats_tmpl()}
    def tmpl():
        return {'all': [], 'total': 0, 'good_rssi_macs': [], 'good_rssi': 0, 'low_rssi_macs': [], 'low_rssi': 0, 'i1_rssi_macs': [], 'i1_rssi': 0, 'i2_rssi_macs': [], 'i2_rssi': 0, 'i3_rssi_macs': [], 'i3_rssi': 0, 'i4_rssi_macs': [], 'i4_rssi': 0, 'i5_rssi_macs': [], 'i5_rssi': 0, 'sig_avg': 0, 'intervals': {'i1': metrics_tmpl(), 'i2': metrics_tmpl(), 'i3': metrics_tmpl(), 'i4': metrics_tmpl(), 'i5': metrics_tmpl()}, 'global': metrics_tmpl(), 'good': metrics_tmpl()}
    for idx, ssid in data['WiFi']['SSID'].items():
        band = data['WiFi']['SSID'][idx]['band']
        if not data['to_band'][band].get('ssid'):
            data['to_band'][band]['ssid'] = {}
        n = data['to_band'][band]['ssid'][idx] = {}
        ads = ssid.get('AssociatedDevice', {}).values()
        ss = [
            {
                'SignalStrength'      : int(a.get('SignalStrength', 0)),
                'OperatingStandard'   : a.get('OperatingStandard', '---'),
                'LastDataDownlinkRate': int(a.get('LastDataDownlinkRate', 0)),
                'LastDataUplinkRate'  : int(a.get('LastDataUplinkRate', 0)),
                'MACAddress'          : a.get('MACAddress', ''),
                'AuthenticationState' : a.get('AuthenticationState', '---'),
                'vendor'              : a.get('vendor') if a.get('vendor') else vendor(a.get('MACAddress', '')),
                'Active'              : a.get('Active', '---'),
                'ipaddress'           : a.get('IPAddress', '---'),
                'AssociationTime'     : a.get('AssociationTime', '---'),
                'Noise'               : int(a.get('Noise', 0)),
                'snr'                 : (int(a.get('SignalStrength', 0)) - int(a.get('Noise', 0))) \
                        if int(a.get('SignalStrength', 0)) and int(a.get('Noise', 0)) else 0,
                'HostName'            : a.get('HostName', '---'),
                'Type'                : a.get('Type',),
                'Retransmissions'    : int(a.get('Retransmissions', 0)),
                'Stats': {
                    'BytesSent'      : int(a.get('Stats', {}).get('BytesSent', 0)),
                    'BytesReceived'  : int(a.get('Stats', {}).get('BytesReceived', 0)),
                    'PacketsSent'    : int(a.get('Stats', {}).get('PacketsSent', 0)),
                    'PacketsReceived': int(a.get('Stats', {}).get('PacketsReceived', 0)),
                    'ErrorsSent'     : int(a.get('Stats', {}).get('ErrorsSent', 0)),
                    'ErrorsReceived' : int(a.get('Stats', {}).get('ErrorsReceived', 0)),
                    'RetransCount'   : int(a.get('Stats', {}).get('RetransCount', 0)),
                }
            }
            for a in ads
        ]
        ss = sorted(
            list(filter(is_active_assoc_dev, ss)), key=itemgetter('SignalStrength'),
        )
        c = n['clients'] = tmpl()
        if ss:
            c['sig_avg'] = sum([s['SignalStrength'] for s in ss]) / len(ss)
            c['total'] = len(ss)
            for s in ss:
                c['all'].append(s)
                val = s['SignalStrength']
                ma = s['MACAddress']
                lddr = s['LastDataDownlinkRate']
                ldur = s['LastDataUplinkRate']
                esent = s['Stats']['ErrorsSent']
                erec = s['Stats']['ErrorsReceived']

                if val >= -30 and val < 0:
                    int_key = 'i1'
                    c['good_rssi'] += 1
                    c['i1_rssi'] += 1
                    if ma:
                        c['good_rssi_macs'].append(ma)
                        c['i1_rssi_macs'].append(ma)
                elif val >= -67 and val < -30:
                    int_key = 'i2'
                    c['good_rssi'] += 1
                    c['i2_rssi'] += 1
                    if ma:
                        c['good_rssi_macs'].append(ma)
                        c['i2_rssi_macs'].append(ma)
                elif val >= -70 and val < -67:
                    int_key = 'i3'
                    c['good_rssi'] += 1
                    c['i3_rssi'] += 1
                    if ma:
                        c['good_rssi_macs'].append(ma)
                        c['i3_rssi_macs'].append(ma)
                elif val >= -80 and val < -70:
                    int_key = 'i4'
                    c['low_rssi'] += 1
                    c['i4_rssi'] += 1
                    if ma:
                        c['low_rssi_macs'].append(ma)
                        c['i4_rssi_macs'].append(ma)
                elif val < -80:
                    int_key = 'i5'
                    c['low_rssi'] += 1
                    c['i5_rssi'] += 1
                    if ma:
                        c['low_rssi_macs'].append(ma)
                        c['i5_rssi_macs'].append(ma)
                else:
                    continue

                if lddr:
                    c['intervals'][int_key]['lddr']['all'].append(lddr)
                if ldur:
                    c['intervals'][int_key]['ldur']['all'].append(ldur)
                if esent:
                    c['intervals'][int_key]['esent']['all'].append(esent)
                if erec:
                    c['intervals'][int_key]['erec']['all'].append(erec)

            # interval stats
            global_lddr = c['global']['lddr']['all']
            global_ldur = c['global']['ldur']['all']
            global_esent = c['global']['esent']['all']
            global_erec = c['global']['erec']['all']
            good_lddr = c['good']['lddr']['all']
            good_ldur = c['good']['ldur']['all']
            good_esent = c['good']['esent']['all']
            good_erec = c['good']['erec']['all']

            for interval in ['i1', 'i2', 'i3', 'i4', 'i5']:
                global_lddr += c['intervals'][interval]['lddr']['all']
                global_ldur += c['intervals'][interval]['ldur']['all']
                global_esent += c['intervals'][interval]['esent']['all']
                global_erec += c['intervals'][interval]['erec']['all']
                if interval in ['i1', 'i2', 'i3']:
                    good_lddr += c['intervals'][interval]['lddr']['all']
                    good_ldur += c['intervals'][interval]['ldur']['all']
                    good_esent += c['intervals'][interval]['esent']['all']
                    good_erec += c['intervals'][interval]['erec']['all']

                for metric in ['lddr', 'ldur', 'esent', 'erec']:
                    m = c['intervals'][interval][metric]
                    if m['all']:
                        m['max'] = max(m['all'])
                        m['min'] = min(m['all'])
                        m['mean'] = statistics.mean(m['all'])
                        m['median'] = statistics.median(m['all'])
                        m['stdev'] = 0 if len(m['all']) < 2 else statistics.stdev(m['all'])

            for metric in ['lddr', 'ldur', 'esent', 'erec']:
                m = c['global'][metric]
                if m['all']:
                    m['max'] = max(m['all'])
                    m['min'] = min(m['all'])
                    m['mean'] = statistics.mean(m['all'])
                    m['median'] = statistics.median(m['all'])
                    m['stdev'] = 0 if len(m['all']) < 2 else statistics.stdev(m['all'])
                m = c['good'][metric]
                if m['all']:
                    m['max'] = max(m['all'])
                    m['min'] = min(m['all'])
                    m['mean'] = statistics.mean(m['all'])
                    m['median'] = statistics.median(m['all'])
                    m['stdev'] = 0 if len(m['all']) < 2 else statistics.stdev(m['all'])

        app.debug('Clients statistics', band=band, c=c)
    return data


def is_active_assoc_dev(ad):
    return (
        True
        if (isinstance(ad['SignalStrength'], int) and ad['Active'] not in [False, 0, '0'])
        else False
    )


def vendor(mac):
    return vendors.get(mac.replace('-', '')[:6], '---')


def generate_recommendations(data, **kw):
    """
    Build list of recommendations based on multiple criteria
    - radio settings
    - optimization results
    - band quality
    - connected clients rssi
    - device information
    """
    recommendations = AXTree()
    issues = AXTree()
    clients = AXTree()

    config = kw.get('default', {})

    new_configs = []
    mode_name = data.get('metadata', {}).get('mode', '')
    if kw.get(mode_name): # check if there is module specific mode config
        new_configs.append(kw.get(mode_name))
    if data.get('conf', {}).get('intel.generate_recommendations'): # check if there is a tenant config add tenant and mode_specific
        new_configs.append(data['conf']['intel.generate_recommendations'].get('default', {}))
        new_configs.append(data['conf']['intel.generate_recommendations'].get(mode_name, {}))
    if new_configs: # if new_configs, merge_cofnigs
        config = merge_dict_configs(config, new_configs)

    # Internal CPE Stats
    recommendations['cpe'] = []
    cpe_info = data['DeviceInfo']
    cpe_info_cfg = config.get('resources_threshold')
    weak_threshold_extender_mesh = config.get('weak_threshold_extender_mesh', -60)
    extreme_threshold_extender_mesh = config.get('extreme_threshold_extender_mesh', -10)
    if cpe_info_cfg:
        res = analyze_cpe_stats(cpe_info, cpe_info_cfg)
        if res:
            recommendations['cpe'] = res
    # Check bands available
    bands = [x for x in ('2', '5') if data['to_band'].get(x)]
    # Check issues
    issues = check_issues(data['to_band'], bands, config)

    # Radio Analysis
    occurrences_threshold = config.get('occurrences_threshold', 2)
    for band in bands:
        recommendations[band] = []

        # Security Settings
        sec_settings = data['to_band'][band]['SSID']
        bad_enc = config.get('bad_encryptions', [])
        bad_sec = config.get('bad_sec_modes', [])
        if sec_settings and (bad_enc or bad_sec):
            res_sec = analyze_security_settings(sec_settings, bad_enc, bad_sec)
            recommendations[band].extend(res_sec)

        # Operating Standards
        op_std_settings = data['to_band'][band]['Radio']
        bad_std = config.get('bad_op_standards', {}).get(band)
        if op_std_settings and bad_std:
            res_op_std = analyze_op_standard(op_std_settings, band, bad_std)
            recommendations[band].extend(res_op_std)

        ssids = data['to_band'][band].get('ssid')
        if ssids:
            # Clients Coverage Analysis
            ssids_band_aggr = data.get('aggregations', {}).get(band, {}).get('ssid', {})
            res_cov = analyze_coverage(ssids, ssids_band_aggr, occurrences_threshold)
            recommendations[band].extend(res_cov)

            # Clients Standard Analysis
            bad_std = config.get('bad_op_standards', {}).get(band)
            if bad_std:
                res_std = analyze_clients_standards(ssids, bad_std)
                recommendations[band].extend(res_std)

        # Extender & Mesh Coverage
        for ssid_index, this_ssid in data['to_band'][band].get('ssid', {}).items():
            for ad in this_ssid.get('clients', {}).get('all', {}):
                if ad.get('Type') in ['Extender', 'Mesh']:
                    if ad.get('SignalStrength', 0) < weak_threshold_extender_mesh:
                        # add recommendations
                        recommendations[band].append({
                            'type': 'extender_weak_signal',
                            'value': ad.get('SignalStrength'),
                            'mac': ad['MACAddress'],
                            'subtree': 'radio',
                            'index': '1' if band == '2' else '5'
                        } if ad.get('Type')=='Extender' else {
                            'type': 'mesh_weak_signal',
                            'value': ad.get('SignalStrength'),
                            'mac': ad['MACAddress'],
                            'subtree': 'radio',
                            'index': '1' if band == '2' else '5'
                        })
                    elif ad.get('SignalStrength', 0) > extreme_threshold_extender_mesh:
                        # add recommendations
                        recommendations[band].append({
                            'type': 'extender_extreme_signal',
                            'value': ad.get('SignalStrength'),
                            'mac': ad['MACAddress'],
                            'subtree': 'radio',
                            'index': '1' if band == '2' else '5'
                        } if ad.get('Type')=='Extender' else {
                            'type': 'mesh_extreme_signal',
                            'value': ad.get('SignalStrength'),
                            'mac': ad['MACAddress'],
                            'subtree': 'radio',
                            'index': '1' if band == '2' else '5'
                        })

        # Steering Analysis
        res_steer = analyze_steering(data['to_band'], band, issues)
        recommendations[band].extend(res_steer)

    data['recommendations'] = recommendations
    data['issues'] = issues
    data['recommendations']['ts'] = now()
    return data


def check_issues(to_band, bands, kw):
    issues = AXTree()
    for band in bands:
        _ed = to_band[band].get('expert')
        _qtc = kw.get('quality_thresholds', {}).get(band, {})
        if _ed and _qtc:
            _dq = _ed.get('delta_q', 0)
            _cq = _ed.get('cur_q', 1)
            _tq = _ed.get('target_q', 1)
            issues[band] = {}
            issues[band]['interf'] = 1 if _dq > _qtc['interf']['above_delta_q'] else 0
            issues[band]['perf'] = 1 if _cq < _qtc['perf']['below_cur_q'] and _tq < _qtc['perf']['below_target_q'] else 0
            if not issues[band]:
                del issues[band]
    return issues


def analyze_cpe_stats(info, cfg):
    """
    Checks the DeviceInfo subtree and returns found issues including:
    - high cpu usage
    - high memory usage
    Based on thresholds defined in cfg.
    """
    # usage
    cpu_usage = info.get('ProcessStatus', {}).get('CPUUsage')
    mem_usage = info.get('MemoryStatus', {}).get('usage', 0)
    # thresholds
    cpu_threshold = cfg.get('cpu', 100)
    mem_threshold = cfg.get('memory', 0)
    res = []

    if cpu_usage and cpu_usage > cpu_threshold:
        r = {
            'type': 'cpu_usage',
            'value': cpu_usage,
            'threshold': cpu_threshold,
        }
        res.append(r)
    if mem_usage and mem_usage > mem_threshold:
        r = {

            'type': 'mem_usage',
            'value': mem_usage,
            'threshold': mem_threshold,
        }
        res.append(r)
    return res


def analyze_security_settings(settings, be=[], bm=[]):
    """
    Checks the settings for security issues including
    - Bad encryption modes
    - weak configs
    - WPS enabled
    - Open wifi
    Based on configs introduced in cfg
    """
    res = []
    for idx, cfg in settings.items():
        sec = cfg.get('Security', {})
        if sec:
            enc = cfg['Security'].get('EncryptionMode')
            if enc and enc in be:
                r = {
                    'subtree': 'ssid',
                    'index': idx,
                    'type': 'security_encryption',
                    'value': enc
                }
                res.append(r)
            mode = cfg['Security'].get('ModeEnabled')
            if mode and mode in bm:
                r = {
                    'subtree': 'ssid',
                    'index': idx,
                    'type': 'security_mode',
                    'value': mode
                }
                res.append(r)
            if enc == 'None' or mode == 'None': # Open wifi
                r = {
                        'subtree': 'ssid',
                        'index': idx,
                        'type': 'security_open_wifi',
                        'value': 'No Encryption'
                        }
                res.append(r)
        wps = cfg.get('WPS', {})
        if wps:
            wps_enabled = wps.get('Enable', False)
            pin_config = 'PIN' in wps.get('ConfigMethodsEnabled', '').split(',')
            if wps_enabled and pin_config:
                r = {
                        'subtree': 'ssid',
                        'index': idx,
                        'type': 'security_wps_pin',
                        'value': wps['ConfigMethodsEnabled']
                        }
                res.append(r)
    return res


def analyze_op_standard(settings, b, bs=[]):
    res = []
    op = settings.get('OperatingStandards')
    if op and op in bs:
        r = {
            'type': 'radio_op_standards',
            'value': op,
            'subtree': 'radio',
            'index': '1' if b == '2' else 5
        }
        res.append(r)
    return res


def analyze_coverage(ssids, ssids_aggr, thr):
    res = []
    for idx, ssid in ssids_aggr.items():
        low_rssi_macs_hist = ssids_aggr[idx]\
                                 .get('clients', {})\
                                 .get('low_rssi_macs_last24h', [])
        low_rssi_count = Counter(low_rssi_macs_hist)
        if low_rssi_count:
            low_rssi_macs = ssids[idx].get('clients', {}).get('low_rssi_macs', [])
            bad_cov_macs = {
                ad['MACAddress']: ad['SignalStrength']
                for ad in ssids[idx].get('clients', {}).get('all', [])
                if ad['MACAddress'] in low_rssi_macs and low_rssi_count[ad['MACAddress']] > thr
            }
            if bad_cov_macs:
                r = {
                    'subtree': 'ssid',
                    'index': idx,
                    'type': 'clients_coverage',
                    'value': bad_cov_macs
                }
                res.append(r)
    return res


def analyze_clients_standards(ssids, bad_std):
    res = []
    for idx, ssid in ssids.items():
        clients = ssid.get('clients', {}).get('all', [])
        bad_std_clients = {
            cl.get('MACAddress'): cl.get('OperatingStandard')
            for cl in clients
            if cl.get('OperatingStandard') in bad_std
        }
        if bad_std_clients:
            r = {
                'subtree': 'ssid',
                'index': idx,
                'type': 'clients_op_standards',
                'value': bad_std_clients
            }
            res.append(r)
    return res


def analyze_steering(to_band, b, issues):
    if not issues:
        return []
    res = []
    alt = '5' if b == '2' else '2'
    # Radio Steering
    expert = to_band[b].get('expert', {})
    if expert:
        cur_ch = expert['cur_ch']
        rec_ch = expert['target_radio_ch']
        interf_issue = issues[b]['interf']
        perf_issue = issues[b]['perf']
        perf_issue_alt = issues.get(alt, {}).get('perf', 1)
        if interf_issue:
            r = {
                'type': 'steering_interf',
                'value': {'cur_ch': cur_ch, 'rec_ch': rec_ch},
                'subtree': 'radio',
                'index': '1' if b == '2' else 5
            }
            res.append(r)
        if perf_issue and not perf_issue_alt:
            r = {
                'type': 'steering_perf',
                'value': {'cur_band': b, 'rec_band': alt},
                'subtree': 'radio',
                'index': '1' if b == '2' else 5
            }
            res.append(r)
    # MAC steering
    ssids_band = to_band[b].get('ssid', {})
    for idx, ssid in ssids_band.items():
        clients = ssid.get('clients', {}).get('all', [])
        to_steer_cov = {}
        to_steer_speed = {}
        for cl in clients:
            rssi = cl['SignalStrength']
            mac = cl['MACAddress']
            if b == '2':
                if rssi > -50 and not perf_issue_alt:
                    to_steer_speed.update({mac: rssi})
            elif b == '5':
                if rssi < -70 and not perf_issue_alt:
                    to_steer_cov.update({mac: rssi})
        if to_steer_speed:
            r = {
                'subtree': 'ssid',
                'index': idx,
                'type': 'clients_steering_speed',
                'value': {'cur_band': b, 'rec_band': alt, 'macs': to_steer_speed},
            }
            res.append(r)
        if to_steer_cov:
            r = {
                'subtree': 'ssid',
                'index': idx,
                'type': 'clients_steering_coverage',
                'value': {'cur_band': b, 'rec_band': alt, 'macs': to_steer_cov},
            }
            res.append(r)
    return res


def pme(data, **kw):
    """
    Pattern Matching Engine. Matches the historical info against a current value and
    if the pattern matches (say the diff on two values is greated than a threshold),
    adds the case (including its action (reboot, optimzie) to the pme subtree. If the
    action is "reboot" and the "force" is set to True, it trys to boot the device.
    A forced reconfiguration will result in optimization regardless of `window` config
    `qualify` in NodeRed.

    For samples of comnfigurations, please check the PME module configs in NodeRed
    """
    config = kw.get('default', {})

    new_configs = []
    mode_name = data.get('metadata', {}).get('mode', '')
    # tenant_name = data.get('tenant', {}).get('mode', '')
    if kw.get(mode_name): # check if there is module specific mode config
        new_configs.append(kw.get(mode_name))
    if data.get('conf', {}).get('intel.pme'): # check if there is a tenant config add tenant and mode_specific
        new_configs.append(data['conf']['intel.pme'].get('default', []))
        new_configs.append(data['conf']['intel.pme'].get(mode_name, []))
    if new_configs: # if new_configs, merge_cofnigs
        config = merge_array_configs(config, new_configs)

    if not config:
        return data
    aggr = data.get('aggregations', {})
    if not aggr:
        return data

    detections = AXTree()
    to_band = AXTree(data['to_band'])
    non_to_band_configs = ['DeviceInfo.ProcessStatus.CPUUsage', 'DeviceInfo.MemoryStatus.usage', 'DeviceInfo.MemoryStatus.Free']
    for cfg in config:
        try:
            c = SimpleNamespace(**cfg)

            min_mov_avg = cfg.get('min', float('-inf'))
            max_mov_avg = cfg.get('max', float('inf'))
            acceptable_configs = ['DeviceInfo.ProcessStatus.CPUUsage', 'DeviceInfo.MemoryStatus.usage', 'DeviceInfo.MemoryStatus.Free']
            # Validate config
            if not ((aggr.has_key(c.mov_avg) and to_band.has_key(c.current)) or (c.current in non_to_band_configs)):
                app.debug('PME pair not configured', mov_avg=c.mov_avg, curr=c.current)
                continue

            # Exclusions
            mov_avg_val = round(aggr[c.mov_avg], 3)
            if to_band.has_key(c.current):
                cur_val = to_band[c.current]
            else:
                cur_val = AXTree(data)[c.current]
            cur_val = round(cur_val, 3)
            if mov_avg_val < min_mov_avg:
                app.debug('Moving average below the minimum accepted value - too low to be considered',
                        mov_avg=mov_avg_val,
                        minimum=min_mov_avg)
                continue
            if mov_avg_val > max_mov_avg:
                app.debug('Moving average above the maximum accepted value - too high to be considered',
                        mov_avg=mov_avg_val,
                        maximum=max_mov_avg)
                continue
            if c.operation == 'drop':
                c.relation = 'N/A'
                op_res = cur_val
            if c.operation not in OPS:
                app.warning('Operation not in OPS', operation=c.operation, ops=OPS)
                continue
            if c.relation not in RELATIONS:
                app.warning('Relation not in RELATIONS', relation=c.relation, rels=RELATIONS)
                continue
            # Calculate
            # Operation
            if c.operation == 'avg':  # average of curernt and moving
                op_res = round((cur_val + mov_avg_val) / 2, 3)
            if c.operation == 'ratio':
                op_res = round(cur_val / mov_avg_val, 3)
            elif c.operation == 'diff':
                op_res = round(cur_val - mov_avg_val, 3)
            elif c.operation == 'drop':
                res = (mov_avg_val > c.threshold and cur_val <= c.threshold)

            # Relation
            if c.relation == 'lower':
                res = True if op_res < c.threshold else False
            elif c.relation == 'higher':
                res = True if op_res > c.threshold else False
            elif c.relation == 'equal':
                res = True if op_res == c.threshold else False

            # Manipulations
            display_function = cfg.get('display_function', None)
            if display_function == 'percent':
                mov_avg_val = f'{round(mov_avg_val)}%'
                op_res = f'{round(op_res)}%'
                c.threshold = f'{round(c.threshold)}%'
            elif display_function == 'higher_than_percent':
                c.threshold = f'> {int(abs(c.threshold) * 100)}%'
                mov_avg_val = f'{int(abs(mov_avg_val) * 100)}%'
                op_res = f'{int(abs(op_res) * 100)}% Drop'


            if res:
                tp = c.current.split('.')[0]
                if not detections.get(tp):
                    detections[tp] = []
                detections[tp].append({
                    'name'            : c.name,
                    'source'          : 'cpe' if tp == 'DeviceInfo' else tp,
                    'action'          : c.action,
                    'operation'       : c.operation,
                    'relation'        : c.relation,
                    'calculated_value': op_res,
                    'moving_average'  : mov_avg_val,
                    'threshold'       : c.threshold,
                    'description'     : cfg.get('description', 'Please add description in NodeRed PME node'),
                    'elastic_id'      : cfg.get('elastic_id', c.name.split('.')[-1]),
                    'enforce'         : cfg.get('enforce', False),
                    'title'           : cfg.get('title', c.name),
                })
        except Exception as ex:
            app.warning('PME misconfiguration detected', ex=ex)
            continue

    if detections:
        data['pme'] = detections
        data['pme']['ts'] = now()
    return data


def axwifi_score(data, **kw):
    config = kw.get('config', {})
    rec = data.get('recommendations', {})
    to_band = data.get('to_band', {})

    if not config or not rec or not to_band:
        return data

    # Initial AXWIFI Score of 100 pp
    AS = 100

    # CPE Recommendations
    for rcpe in rec['cpe']:
        AS = AS - config['cpe'][rcpe['type']]

    # Check bands available
    bands = [x for x in ('2', '5') if data['to_band'].get(x)]

    # Radio Recommendations
    for cr in config['radio']:
        try:
            c = 0
            points = 0
            for band in bands:
                for rb in rec[band]:
                    if rb['type'] in cr['type']:
                        c = c + 1

            for crt in cr['threshold']:
                if c >= crt:
                    points = (cr['threshold'].index(crt)+1)*cr['points']

            AS = AS - points

        except Exception as ex:
            app.error('AXWIFI Score | radio misconfiguration detected', ex=ex)
            continue

    # Clients Recommendations
    clients = 0
    # calculate #no of all clients
    for band in bands:
        for ssid in to_band[band]['ssid']:
            clients = clients + to_band[band]['ssid'][ssid]['clients']['total']

    if clients > 0:
        for cc in config['clients']:
            try:
                c = 0
                points = 0
                for band in bands:
                    for rb in rec[band]:
                        if rb['type'] in cc['type']:
                            if rb['type'].startswith('clients_steering'):
                                c = c + len(rb['value']['macs'])
                            else:
                                c = c + len(rb['value'])

                for cct in cc['threshold']:
                    if (c / clients * 100) >= cct:
                        points = cc['points']
                        AS = AS - points

            except Exception as ex:
                app.error('AXWIFI Score | clients misconfiguration detected', ex=ex)
                continue

    val = {'value': AS}
    data['score'] = val
    return data


class Operators:
    inspect_clients = inspect_clients
    identify_changes = identify_changes
    inspect_hosts = inspect_hosts
    calculate_radio_stats = calculate_radio_stats
    generate_recommendations = generate_recommendations
    pme = pme
    axwifi_score = axwifi_score
    identify_associateddevices = identify_associateddevices
    inspect_ieee1905 = inspect_ieee1905
