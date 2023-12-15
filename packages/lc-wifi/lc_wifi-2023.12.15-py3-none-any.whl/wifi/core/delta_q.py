import re
from operators.core import ax_core_ops
from operators.con import con

import baseG5  # noqa
import baseG2  # noqa

ax = ax_core_ops

algos_qual = {'2': baseG2.channel_quality, '5': baseG5.channel_quality}
algos_select = {'2': baseG2.greedy_calc, '5': baseG5.bw_select}


def delta_q(data, fingerprinting=True):
    """
    reading a TR-181 normalized, F/A stamped single reading.
    """
    for b in '2', '5':
        _delta_q(data, b, fingerprinting)


def _delta_q(reading, band, fingerprinting):
    """b = 2 or 5"""
    r = reading['to_band'][band]
    scan = r.get('scan', None)
    radio = r['Radio']
    if scan is None or radio is None or not radio.get('enabled'):
        return

    hosts_macs = reading.get('tmp', {}).get('hosts_macs', [])

    # prepare data for algos
    env = []
    for idx, n in scan.items():
        tp = 'A'
        if fingerprinting:
            # if False we save a lot of load on redis:
            fp_key = 'fingerprints:' + n['BSSID'] + '_' + str(n['radio_chan'])
            res = con.redis.get(reading, msg=None, key=fp_key)
            if res == {'payload': band}:
                tp = 'F'
        tp = 'E' if tp == 'A' and detect_extender(n['BSSID'], *hosts_macs) else tp
        m = {
            'bandwidth': n['bandwidth'],
            'channel': n['radio_chan'],
            'rssi': n['rssi'],
            'type': tp,
        }
        scan[idx]['type'] = tp
        env.append(m)

    # get qualities per channel for display purposes
    channel_quality = algos_qual[band]
    kw = {} if band == '2' else {'bw': radio['bandwidth'], 'rch': radio['radio_chan']}
    chan_quals = {
        str(chan): channel_quality(chan, env, remove_radar=True, **kw)
        for chan in radio['possible_channels']
    }
    res = reading['to_band'][band]['expert'] = {
        'algo': 'greedy',
        'qualities': chan_quals,
    }

    # get recommended settings
    select_best = algos_select[band]
    country = reading['conf'].get('country')
    # add current and target settings to results
    res['cur_bw'] = radio['bandwidth']
    res['cur_ch'] = res['cur_radio_ch'] = radio['radio_chan']
    if band == '2':
        max_cfg_ch = reading['conf'].get('upper_chan_2', 13)
        max_pc = max(radio['possible_channels'])
        radio['upper_channel'] = max_cfg_ch if max_cfg_ch <= max_pc else max_pc
        best_ch, best_q = select_best(radio, env)
        best_bw = 'Auto'
        res['target_radio_ch'] = res['target_ch'] = best_ch
    if band == '5':
        if res['cur_bw'] in (40, 80, 160):
            res['cur_ch'] = baseG5.ch_5G.ch_map.get(res['cur_bw'], {}).get(
                res['cur_radio_ch']
            )
        if res['cur_radio_ch'] >= 52:
            res['cur_on_dfs'] = True
        best_ch, best_q, best_bw = select_best(radio, env, country)
        res['target_radio_ch'] = res['target_ch'] = best_ch
        if best_bw in (40, 80, 160):
            res['target_ch'] = baseG5.ch_5G.ch_map.get(best_bw, {}).get(best_ch)
    res['target_q'] = best_q
    res['target_bw'] = best_bw

    # get neighbors statistics
    res['neighbors'] = _neighbors_stats(band, radio, env)
    res['neighbors']['all'] = env

    # determine delta quality
    res['cur_q'] = cur_q = res['qualities'].get(str(radio['radio_chan']), 0)
    res['delta_q'] = best_q - cur_q

    return reading


def detect_extender(bssid, *args):
    bssid_octets = [bo.upper() for bo in re.split(r':|-', bssid)]
    for mac in args:
        mac_octets = [mo.upper() for mo in re.split(r':|-', mac)]
        x = 0
        for i in range(0, 5):
            if bssid_octets[i] == mac_octets[i]:
                x += 1
        if x >= 3:
            return True
    return False


def _neighbors_stats(b, radio, data):
    chan = radio['radio_chan']
    bw = radio['bandwidth']
    friends = 0
    extenders = 0

    if b == '2':
        min_rssi = baseG2.MIN_RSSI
        adj_data = []
        co_data = []
        if len(data) != 0:
            for cpe in data:
                if cpe['type'] == 'F':
                    friends += 1
                if cpe['type'] == 'E':
                    extenders += 1
                channel_diff = abs(chan - cpe['channel'])
                if channel_diff >= 5 and bw == 20 and cpe['bandwidth'] == 20:
                    continue
                if (
                    channel_diff >= 7
                    and (bw == 40 and cpe['bandwidth'] == 20)
                    and (bw == 20 and cpe['bandwidth'] == 40)
                ):
                    continue
                if channel_diff >= 9:
                    continue
                if cpe['rssi'] < min_rssi:
                    continue
                if cpe.get('associated_devices', None) == 0:
                    continue
                if channel_diff == 0:
                    co_data.append(cpe)
                    continue
                adj_data.append(cpe)

        t = len(data)
        aci = len(adj_data)
        cci = len(co_data)
        return {
            'total': t,
            'aci': aci,
            'cci': cci,
            'aci_cci': cci + aci,
            'friends': friends,
            'extenders': extenders,
        }

    if b == '5':
        rssi_limit = baseG5.RSSI_LIMIT
        bw = radio['bandwidth']
        interf = []
        not_interf = []
        if len(data) != 0:
            for cpe in data:
                if cpe['type'] == 'F':
                    friends += 1
                if cpe['type'] == 'E':
                    extenders += 1
                if cpe['rssi'] < rssi_limit:
                    continue
                if cpe.get('associated_devices', None) == 0:
                    continue
                if cpe['bandwidth'] == 20:
                    wlan_chan = cpe['channel']
                else:
                    wlan_chan = baseG5.ch_5G.ch_map.get(cpe['bandwidth']).get(
                        cpe['channel']
                    )
                interfering_channels = baseG5.ch_5G.IF_5G.get(chan, {})
                if wlan_chan in interfering_channels.keys():
                    interf.append(cpe)

        t = len(data)
        interfering = len(interf)
        return {
            'total': t,
            'interfering': interfering,
            'friends': friends,
            'extenders': extenders,
        }
