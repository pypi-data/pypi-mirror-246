LAYER1 = {
                'repeater': 'Device.WiFi.Radio',
                '2.4G': 'Device.WiFi.Radio.1',
                '5G': 'Device.WiFi.Radio.5',
                'none': 'Device.Ethernet'
        }

TRUES = {1, '1', True, 'true'}

def to_hosts(data, msg):
    mesh = data.get('Huawei', {}).get('Mesh')
    hosts = data.get('Hosts', {}).get('Host')
    if not (mesh and hosts):
        return data

    # map mac to host idx
    hosts_idxs = { h['PhysAddress']: i for i, h in hosts.items() }
    # set mac address as key to mesh node for active nodes
    new_mesh = { node['hw_mesh_mac']: node for i, node in mesh.items() if node['hw_mesh_status'] in TRUES }

    for mac, node in new_mesh.items():
        hidx = hosts_idxs[mac]
        host = hosts[hidx]
        host['DeviceID'] = node['hw_mesh_uuid']
        host['ModelName'] = node['hw_mesh_device_type']
        host['Manufacturer'] = 'Huawei' if node['hw_mesh_device_type'].startswith('HG') else 'Unknown'
        host['Mode'] = node['hw_mesh_working_mode']
        wlans = node.get('hw_mesh_wlans', {})
        if wlans:
            host['Layer1Interface'] = LAYER1['repeater']
        for wlan in wlans.values():
            if wlan['AssociatedDeviceNumberOfEntries']:
                for ad in wlan['AssociatedDevice'].values():
                    m = ad['AssociatedDeviceMACAddress'].replace(':', '-')
                    # update hosts tree
                    hidx_clt = hosts_idxs[m]
                    host_clt = hosts[hidx_clt]
                    typ = wlan.get('RFBand', 'none')
                    layer1int = LAYER1[typ]
                    new_params = {
                            'ParentNodeID': host['DeviceID'],
                            'SignalStrength': int(ad['RSSI']),
                            'LastDataDownLinkRate': int(ad['TxRate']),
                            'LastDataUplinkRate': int(ad['RxRate']),
                            'Layer1Interface': layer1int,
                    }
                    host_clt.update(new_params)
    return data

class Operators:
    to_hosts = to_hosts
