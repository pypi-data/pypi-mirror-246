#!/usr/bin/env python
import os, sys, time, uuid
from devapp.app import run_app, app
from functools import partial as p


# ------------------------------------------------- taken from the old non nod-red one.
# TODO: fix this
import re
import time
from devapp.app import app
from wifi.vendors.vendors import vendors
from operator import itemgetter
from wifi.core.delta_q import delta_q
import ch_5G


class C:
    """cache"""

    OpStd = {'2': {}, '5': {}}
    PosChans = {}


def fix_radio_refs(data):
    """
    .Radio gets 2, 5 set like: {2: '2', '2': {'OperatingFr.B': '2.4GHz', ..}
    -> Fast lookups of radio later. Plus verify of data sanity.
    """
    r = data
    refs = {}
    rad = r['WiFi']['Radio']
    _ = r['WiFi']['SSID']
    _ = r['DeviceInfo']['SerialNumber']
    for k, radio in rad.items():
        if k == 'wifi_fingerprint':
            continue
        if not isinstance(radio, dict):
            continue
        if 'AutoChannelEnable' not in radio:
            radio['AutoChannelEnable'] = 1
            radio['mocked_auto_chan_enable'] = 1

        radio['possible_channels'] = chs = lookup(
            'PossibleChannels',
            C.PosChans,
            supported_radio_chans,
            radio,
            conf=data.get('conf', {}),
        )
        b, ch, enabled = normalize_radio(radio, idx=k)
        if ch and chs and ch not in chs:
            app.warn('Not allowed ch', radio=radio)
            radio['enabled'] = False
        if b in ('2', '5'):
            refs[b] = k

    if not refs:
        # raise Exception('No radio refs')
        app.warn('No radio refs')

    # json dump load cycles would turn to string. that will suck.
    # so:
    refs['2'] = refs.pop('2', None)
    refs['5'] = refs.pop('5', None)
    r['WiFi']['RadioRefs'] = refs
    return r


def lookup(key, c, func, radio, **kw):
    # TODO: purpose - why not call directly the func?
    r = c.get(radio.get(key))
    if r is not None:
        return r
    try:
        r = c[key] = func(radio, **kw)
    except Exception as ex:
        app.error('Lookup exception', ex=ex)
    return r


dash_sepped_chans = re.compile(r'(?P<s>\d+)\-(?P<e>\d+)')
comma_sepped_chans = re.compile(r'^\d+(,\d+)*$')
# TODO:  UDI for this....
dflt_possible_chans_5 = [
    36,
    40,
    44,
    48,
    52,
    56,
    60,
    64,
    100,
    104,
    108,
    112,
    116,
    132,
    136,
]


def supported_radio_chans(radio, conf, r1=dash_sepped_chans, r2=comma_sepped_chans):
    pc = radio.get('PossibleChannels')
    if not pc:
        if '2' in radio.get('OperatingFrequencyBand'):
            uc = conf.get('upper_chan_2', 13)
            r = [i for i in range(uc + 1)]
        else:
            r = conf.get('possible_chan_5', dflt_possible_chans_5)
        app.warning('No PossibleChannels reported by device - adding default', chans=r)
        return r

    if pc:
        if r1.search(pc):
            m = r1.search(pc)
            s = int(m.group('s'))
            e = int(m.group('e'))
            return [i for i in range(s, e + 1) if i != 0]
        if pc.endswith(','):
            pc = pc[:-1]
        if r2.search(pc):
            cs = [c.strip() for c in pc.split(',')]
            return [
                int(i)
                for i in cs
                if i
                not in (
                    0,
                    '0',
                )
            ]
    return []


def op_standard(radio):
    os = radio.get('OperatingStandards', '')
    numbers = {
        '2': [['n', 4], ['g', 3], ['b', 2]],
        '5': [['ax', 7], ['ac', 6], ['n', 5]],
    }
    for std, nr in numbers[radio['band']]:
        if std in os:
            return nr
    return 1


disabled = None, None, False


def normalize_scan_result(r):
    nwd = 'NeighboringWiFiDiagnostic'
    nwd = r['WiFi'].get(nwd)
    if not nwd:
        return r
    if r['WiFi']['Radio'].get('1') and r['WiFi']['Radio']['1'].get('enabled'):
        nwd['2'] = {}
    if r['WiFi']['Radio'].get('5') and r['WiFi']['Radio']['5'].get('enabled'):
        nwd['5'] = {}
    scan = nwd.get('Result') or {}
    for k, v in scan.items():
        b, ch, enabled = normalize_radio(v)
        if enabled and b in nwd:
            nwd[b][k] = v
    nwd.pop('Result', 0)
    return r


def normalize_radio(radio, idx=None):
    """for radios AND neighbours, then idx is None"""
    rd_enabled = radio.get('Enable', True)
    rd_status = 1 if radio.get('Status', 'Up').lower() == 'up' else 0
    enabled = True if rd_enabled and rd_status else False
    # if (not enabled or not status):
    #    return disabled
    # if not enabled and not idx:
    #    return disabled
    ch = radio.get('Channel')
    try:
        ch = int(ch)
    except Exception:
        app.warn('Channel problem', ch=ch)
        ch = 0

    if idx is None:
        try:
            _ = radio['rssi'] = int(radio['SignalStrength'])
            if _ < -255 or _ >= 0:
                raise
        except Exception:
            app.warn('RSSI problem', radio=radio)
            return disabled
            radio['rssi'] = 0

        try:
            _ = radio['noise'] = int(radio['Noise'])
            if _ < -255 or _ >= 0:
                raise
        except Exception:
            # report_warn('Noise problem', radio)
            # return disabled
            radio['noise'] = None

        try:
            _ = radio['snr'] = int(radio['rssi'] - radio['noise'])
            if _ > 255 or _ <= 0:
                raise
        except Exception:
            radio['snr'] = None

    if idx:
        try:
            _ = radio['noise'] = int(radio['Stats']['Noise'])
            if _ < -255 or _ >= 0:
                raise
        except Exception:
            # report_warn('Noise problem', radio)
            radio['noise'] = 0

    if ch > 0 and ch < 15 and enabled:
        b = '2'
    elif ch > 35 and ch < 166 and enabled:
        b = '5'
    else:
        # ch, enabled = 0, False
        opw = radio.get('OperatingFrequencyBand', '')
        if opw.startswith('2.4') or idx == '1':
            b = '2'
        elif opw.startswith('5') or idx == '5':
            b = '5'
        else:
            raise Exception('No band', radio)

    radio['enabled'] = enabled
    radio['band'] = b
    if enabled:
        radio['radio_chan'] = ch
        if b == '5':

            def f(x):
                return ch_5G.ch_map.get(x)

            radio_channels = []
            for m in list(map(f, [40, 80, 160])):
                for k, v in m.items():
                    if v == ch:
                        radio_channels.append(k)
            if radio_channels:
                # bad assumption, but we can't determine exact one
                radio['radio_chan'] = radio_channels[0]

        o = str(radio.get('OperatingChannelBandwidth')).lower().split('mhz')[0]
        try:
            if b == '5':
                w = 80 if (o in ('auto', 'none', '20/40/80')) else int(o)
                assert w in (20, 40, 80, 160)
            else:
                w = 20 if (o in ('auto', 'none', '20/40')) else int(o)
                assert w in (20, 40)
        except Exception as ex:
            app.warn('Channel Width Problem', radio=radio)
            w = 0
            # report_warn('No OperatingChannelBandwidth', r)
        radio['bandwidth'] = w
        radio['op_standard'] = lookup(
            'OperatingStandards', C.OpStd[b], op_standard, radio
        )
    return b, ch, enabled


def band_into_ssids(r):
    rad, refs = r['WiFi']['Radio'], r['WiFi']['RadioRefs']
    rrefs = {refs.get('2'): '2', refs.get('5'): '5'}
    n = {}
    for idx, ssid in r['WiFi']['SSID'].items():
        ll = (ssid.get('LowerLayers') or '.%s' % idx).rsplit('.', 1)[-1]
        band = rrefs.get(ll)
        if not band:
            app.err('Lower layer ref broken', data=r)
            continue
        ssid['band'] = band
        n[idx] = ssid
    r['WiFi']['SSID'] = n
    return r


def access_points_into_ssids(r):
    """Moving the AP data into their SSID
    WE DO THIS IN THE TR181 TREE!
    (no specific reason, just too much data. purist vs. practicabilty)
    """
    aps = r['WiFi']['AccessPoint']
    ssids = r['WiFi']['SSID']
    for idx, ap in aps.items():
        sidref = ap.get('SSIDReference') or 'Device.WiFi.SSID.%s' % idx
        sidx = sidref.rsplit('.', 1)[-1]
        ssid = ssids.get(sidx)
        if not ssid:
            app.warn('SSID ref not found', data=r)
        else:
            ssid.update(ap)
    return r


class Operators:
    fix_radio_refs = fix_radio_refs
    normalize_scan_result = normalize_scan_result
    access_points_into_ssids = access_points_into_ssids
    band_into_ssids = band_into_ssids
    delta_q = delta_q
