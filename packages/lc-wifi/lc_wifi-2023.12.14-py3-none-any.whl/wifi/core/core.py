#!/usr/bin/env python

from wifi.core import expert, intel
from wifi.vendors import avm, huawei
from wifi.test.test import test
import time
import math

from operators.kv_tools import kv
from operators.con import con

from gevent.event import Event


from node_red import nrclient as red
from devapp.app import run_app, app
from devapp.tools import into, get_deep
from functools import partial

# from axlib.ax_tree.ax_tree import AXTree
from ax.utils.ax_tree import AXTree


from operators.core import ax_core_ops

ax = ax_core_ops


now = time.time

AGGREGATE_STD_KEYS = ['src', 'dst', 'cf', 'age']


def get_radio(band, r, get_idx=None):
    w = r['WiFi']
    rad, ref = w['Radio'], w['RadioRefs']
    return rad.get(ref.get(band))


def loop_for_value(d, full_key):
    split_key = full_key.split('.')
    for k in split_key:
        d = d.get(k, {})
        if d == {}:
            break
    return d


def parse_agg_cfg(cfg):
    min_cfg = {}
    for c in cfg:
        if list(c) != AGGREGATE_STD_KEYS:
            continue

        src = c['src']
        dst = c['dst']
        cf = c['cf']
        age = c['age']

        if src not in min_cfg.keys():
            min_cfg[src] = {'entries': [(dst, cf, age)], 'values': []}
        else:
            min_cfg[src]['entries'].append((dst, cf, age))

    for k, v in min_cfg.items():
        min_cfg[k]['max_age'] = max([a[2] for a in v['entries']])

    return min_cfg


def cache_entries(cfg, hist):
    for msg_data in hist:
        msg = AXTree(msg_data[1])
        ts = msg['ts']
        for ck, cv in cfg.items():
            if ts < now() - cv['max_age']:
                break
            value = msg.get(ck)
            if value is not None:
                cv['values'].append((ts, value))


def calc_avg(values):
    values_len = len(values)
    try:
        return sum(values) / float(values_len)
    except ZeroDivisionError:
        return None


def calc_sum(values):
    try:
        return sum(values)
    except Exception:
        return None


def calc_max(values):
    try:
        return max(values)
    except Exception:
        return None


def calc_min(values):
    try:
        return min(values)
    except Exception:
        return None


def calc_std_dev(values):
    try:
        avg = calc_avg(values) or 0
        variance = sum([(v - avg) ** 2 for v in values]) / len(values)
        return math.sqrt(variance)
    except ZeroDivisionError:
        return None


def calc_concat(values):
    import itertools

    return list(itertools.chain(*values))


def parse_pme(dt, r):
    def tmpl(x):
        return {
            'all': [],
            'total': 0,
            'detail': {},
            'ts': dt[x].get('ts', time.time()),
        }

    for k, v in dt['pme'].items():
        if k == 'ts':
            continue
        if k == 'DeviceInfo':
            k = 'cpe'
        if k == 'cpe' and not r.has_key(k):
            r[k] = {}
        pme = tmpl('pme')
        pme['all'] = all_pme = v
        pme['total'] = len(v)
        for a in all_pme:
            tp = a['elastic_id']
            detail = pme['detail']
            if tp not in detail:
                detail[tp] = 0
            detail[tp] += 1
        r[k]['pme'] = pme
    return r


def parse_rec(dt, r):
    def tmpl(x, band):
        details = {
            'cpe': {'cpu_usage': 0, 'mem_usage': 0},
            '2': {
                'clients_op_standards': 0,
                'clients_steering_speed': 0,
                'clients_steering_coverage': 0,
                'clients_coverage': 0,
                'steering_interf': 0,
                'steering_perf': 0,
                'radio_op_standards': 0,
                'security_mode': 0,
                'security_encryption': 0,
                'security_open_wifi': 0,
                'security_wps_pin': 0,
                'extender_weak_signal': 0,
                'mesh_weak_signal': 0,
                'extender_extreme_signal': 0,
                'mesh_extreme_signal': 0,
            },
            '5': {
                'clients_op_standards': 0,
                'clients_steering_speed': 0,
                'clients_steering_coverage': 0,
                'clients_coverage': 0,
                'steering_interf': 0,
                'steering_perf': 0,
                'radio_op_standards': 0,
                'security_mode': 0,
                'security_encryption': 0,
                'security_open_wifi': 0,
                'security_wps_pin': 0,
                'extender_weak_signal': 0,
                'mesh_weak_signal': 0,
                'extender_extreme_signal': 0,
                'mesh_extreme_signal': 0,
            },
        }
        return {
            'all': [],
            'total': 0,
            'detail': details[band],
            'ts': dt[x].get('ts', time.time()),
        }

    if 'cpe' not in r:
        r['cpe'] = {}
    r['cpe']['recommendations'] = tmpl('recommendations', 'cpe')
    r['2']['recommendations'] = tmpl('recommendations', '2')
    r['5']['recommendations'] = tmpl('recommendations', '5')
    for k, v in dt.get('recommendations', {}).items():
        if k == 'ts':
            continue
        r[k]['recommendations']['all'] = all_rec = v
        r[k]['recommendations']['total'] = len(v)
        for a in all_rec:
            tp = a['type']
            if tp not in r[k]['recommendations']['detail']:
                r[k]['recommendations']['detail'][tp] = 0
            r[k]['recommendations']['detail'][tp] += 1
    return r


now = time.time


class Event(Event):
    pass


class WiFiFunctions:
    test = test
    _jobs = {}

    # default mapping - func name convention:
    expert = expert.Operators
    intel = intel.Operators
    avm = avm.Operators
    huawei = huawei.Operators

    def configs_by_tenant(data, **kw):
        if not kw:
            return data

        tenant = get_deep('props.metadata.tenant', data, dflt=False)
        if not tenant:
            return data

        conf = kw.get(tenant)
        if not conf:
            app.warn('Tenant not configured', tenant=tenant, op='configs_by_tenant')
            return data
        conf['tenant_id'] = tenant
        kv.update(data, msg={}, pth=['conf'], deep=False, create=True, **conf)
        return data

    class join:
        def combine_tr069_with_avm_json(have, json_data):
            try:
                tr069 = have['payload']
                json_data = json_data['payload']
                method = json_data['props']['data']['upload_method']
                have['payload'] = avm.parse_and_merge(tr069, json_data, method)
            except Exception as _:
                _ = 'Cannot merge avm tr069 with json data (missing json data for json nr 2 or 3)'
                raise Exception(_) from None
            return have

        def id_from_kafka_or_json(msg):
            p = msg['payload']
            return p.get('id') or p.get('cpeid')

    def validate_and_arrange_data(data, max_age=60):
        p = data.pop('props', 0)
        # automillis (node red timestamper does millis)
        ts = data['ts']
        if ts > 9999999999:
            data['ts'] = ts / 1000.0
        if 0 and now() - data['ts'] > max_age:
            return (
                'exception',
                'record outdated (%2d sec)' % (now() - data['ts']),
            )

        # already right format?
        if p != 0:
            # from real axtract
            data.update(p)
            data['id'] = data.pop('cpeid', 0)

    def to_band(data):
        tb = data['to_band'] = {'2': None, '5': None}
        fps = data['fingerprints'] = {}
        for b in '2', '5':
            """We add a band specific normalized submap"""
            m = {'band': b}
            wifi = data.get('WiFi', {})
            rid = data['id']
            m['rid'] = rid

            # config:
            m['Radio'] = get_radio(b, data)
            # FIXME: bug workaround with 5 else (got 2)
            ns = [s for s in wifi['SSID'].values() if s['band'] == b]
            # handy for later inserts:
            [into(n, 'rid', rid) for n in ns]
            k = 1 if b == '2' else 5
            m['SSID'] = {}
            fingerprints = {}
            for ssid in ns:
                m['SSID'][str(k)] = ssid
                fp = m['SSID'][str(k)]['BSSID'] + '_' + str(m['Radio']['Channel'])
                fingerprints[fp] = b
                k += 1

            # scan state:
            try:
                nwd = 'NeighboringWiFiDiagnostic'
                m['scan'] = wifi[nwd].pop(b, [])
                m['scan_dt'] = wifi[nwd].get('coll_dt', 0)
            except Exception as _:
                app.debug('No scan on band', band=b)
            tb[b] = m
            fps.update(fingerprints)

        # write fingerprints to redis
        for f in fps:
            _ = con.redis.set(
                data=data,
                msg=None,
                key='fingerprints:' + f,
                pth='fingerprints.' + f,
            )
        return data

    def normalize_mac(mac, final_sep='-'):
        hex_chars = set('0123456789ABCDEF')
        seps = '.:- '
        clean_len = 12

        if not mac:
            return ''

        mac = str(mac).strip().upper()
        for sep in seps:
            mac = mac.replace(sep, '')

        if len(mac) != clean_len or len(set(mac) - hex_chars):
            return ''

        result = [mac[i : i + 2] for i in range(0, clean_len, 2)]
        return final_sep.join(result)

    def multiap_to_hosts(data):
        # copies mesh devices in MultiAP subtree
        # to the Hosts subtree, with ParentNodeID, for the map

        multiap = data.get('MultiAP')
        if not multiap:
            return data

        # ensure hosts structure exists
        # CPE may not produce it if no devices connected directly
        hosts = data.get('Hosts')
        if hosts is None:
            hosts = data['Hosts'] = {}
        hosts = hosts.get('Host')
        if hosts is None:
            hosts = hosts['Host'] = {}

        # determine next host index
        next_host_idx = int(max(hosts.keys(), key=int, default=0)) + 1

        # prepare dict of existing host mac addresses to check for duplicates
        existing_macs = {
            WiFiFunctions.normalize_mac(host.get('MACAddress')): idx
            for idx, host in hosts.items()
        }

        # traverse MultiAP structure and add to hosts
        apdevs = multiap.get('APDevice', {})
        for apdev in apdevs.values():
            # add apdev itself?

            ad_parent = WiFiFunctions.normalize_mac(apdev.get('MACAddress'))
            if not ad_parent:
                continue

            radios = apdev.get('Radio', {})
            for radio in radios.values():
                aps = radio.get('AP', {})
                for ap in aps.values():
                    associated_devices = ap.get('AssociatedDevice', {})
                    for associated_device in associated_devices.values():
                        if not associated_device.get('Active', True):
                            # ignore inactive devices
                            # may be active in another AP
                            continue

                        ad_mac = WiFiFunctions.normalize_mac(
                            associated_device.get('MACAddress')
                        )
                        if not ad_mac:
                            continue

                        ad_data = {
                            'ParentNodeID': ad_parent,
                            'DeviceID': ad_mac,
                            'MACAddress': ad_mac,
                        }

                        existing_host_idx = existing_macs.get(ad_mac)
                        if existing_host_idx is not None:
                            # avoid duplicating host, but set ParentNodeID and DeviceID
                            hosts[existing_host_idx].update(ad_data)
                            continue

                        # add new host
                        associated_device.update(ad_data)
                        cur_host_idx = str(next_host_idx)
                        hosts[cur_host_idx] = associated_device
                        existing_macs[ad_mac] = cur_host_idx
                        next_host_idx += 1

        return data

    def data_filter(data, msg, **kw):
        new_data_flat = AXTree()
        for k in kw.get('allow'):
            if data.has_key(k):
                new_data_flat[k] = data[k]
        return new_data_flat

    def calculate_rates(data, **kw):
        calculate = kw.get('calculate', {})
        hist = data.get('history', {}).get('events')
        if not calculate or not hist:
            return data
        data['rates'] = AXTree()

        last = AXTree(hist[0][1])
        params = kw['calculate']
        for param in params:
            prop = param['prop']
            max_diff = param.get('max_diff')
            min_diff = param.get('min_diff')
            max_rate = param.get('max_rate')
            min_rate = param.get('min_rate')
            heartbeat = param.get('heartbeat')
            reset_to_zero = param.get('reset_to_zero')
            if not last.has_key(prop):
                continue
            last_value = last[prop]
            last_ts = last['ts']
            cur_value = loop_for_value(data, prop)
            cur_ts = data['ts']
            # verify constraints
            if cur_value == {}:
                continue
            if min_diff is not None and cur_value - last_value < min_diff:
                if reset_to_zero:
                    data['rates'][prop + 'PerSec'] = 0
                continue
            if max_diff is not None and cur_value - last_value > max_diff:
                if reset_to_zero:
                    data['rates'][prop + 'PerSec'] = 0
                continue
            if heartbeat is not None and cur_ts - last_ts > heartbeat:
                continue
            if cur_ts == last_ts:
                return data
            try:
                rate = (cur_value - last_value) / (cur_ts - last_ts)
            except Exception as ex:
                print('breakpoint set')
                breakpoint()
                keep_ctx = True
            if max_rate is not None and rate > max_rate:
                if reset_to_zero:
                    data['rates'][prop + 'PerSec'] = 0
                continue
            if min_rate is not None and rate < min_rate:
                if reset_to_zero:
                    data['rates'][prop + 'PerSec'] = 0
                continue
            data['rates'][prop + 'PerSec'] = rate
        return data

    def rolling_aggregation(data, **kw):
        config = kw.get('config', {})
        hist = data.get('history', {}).get('events')
        if not hist or not config:
            return data
        data['aggregations'] = AXTree()

        compressed_cfg = parse_agg_cfg(config)
        cache_entries(compressed_cfg, hist)

        for ck, cv in compressed_cfg.items():
            for e in cv['entries']:
                dst, cf, age = e
                values_in_range = []
                for v in cv['values']:
                    ts, val = v
                    if ts < now() - age:
                        break
                    values_in_range.append(val)
                if cf == 'avg':
                    res = calc_avg(values_in_range)
                elif cf == 'sum':
                    res = calc_sum(values_in_range)
                elif cf == 'max':
                    res = calc_max(values_in_range)
                elif cf == 'min':
                    res = calc_min(values_in_range)
                elif cf == 'std_dev':
                    res = calc_std_dev(values_in_range)
                elif cf == 'concat':
                    res = calc_concat(values_in_range)
                else:
                    app.error('CF is not valid for aggregation', ck=ck, cv=cv)
                if res is not None:
                    data['aggregations'][dst] = res

        return data

    def internal_performance_kpis(data):
        """
        This node is used to calculate some KPIs which are needed by the core
        but not provided directly by the device tree; like
        DeviceInfo.MemoryStatus.usage which contains the % of the used memory
        """
        # calculate and populate DeviceInfo.MemoryStatus.usage
        if 'MemoryStatus' not in data['DeviceInfo']:
            data['DeviceInfo']['MemoryStatus'] = {}
        mem_stats = data['DeviceInfo']['MemoryStatus']
        total = mem_stats.get('Total', 100)
        free = mem_stats.get('Free', 100)
        data['DeviceInfo']['MemoryStatus']['usage'] = ((total - free) / total) * 100

        return data

    def arrange_data(data):
        """data into axtract format"""

        def tmpl():
            return {
                'expert': {},
                'recommendations': {},
                'pme': {},
                'changes': {},
                'clients': {},
                'ssid': {},
            }

        # r = {'2': b(), '5': b(), 'WiFi': {'Radio': {'1': {}, '5': {}}}}  # KPIs
        res = AXTree({'2': tmpl(), '5': tmpl()})

        bands = [
            (i, data['to_band'].get(i)) for i in ('2', '5') if data['to_band'].get(i)
        ]

        for b, B in bands:
            m = res[b]['expert']
            exp = B.get('expert')
            # if not radio enabled this is empty:
            if exp:
                if 'denied_by_condition' not in exp:
                    exp['denied_by_condition'] = True
                for e, v in exp.items():
                    if e in {'gbases_raw_res', 'id', 'qualities'}:
                        continue
                    m[e] = v
                m['neighbors']['all'] = [
                    {
                        k.lower(): B['scan'][n].get(k)
                        for k in (
                            'BSSID',
                            'Channel',
                            'SSID',
                            'Noise',
                            'bandwidth',
                            'rssi',
                            'type',
                            'snr',
                        )
                    }
                    for n in B['scan']
                ]
            res[b]['ssid'] = B.get('ssid', {})
            res[b]['changes'] = B.get('changes', {})
            res[b]['clients'] = B.get('clients', {})
            res[b]['pme'] = B.get('pme', {})
            res[b]['issues'] = B.get('issues', {})
            res[b]['Radio'] = B['Radio']
            res[b]['SSID'] = B['SSID']
            res[b]['scan_dt'] = B.get('scan_dt', 0)
            res[b]['count'] = B.get('count', {})
            if data.get('aggregations', {}).get(b):
                res[b].merge(data['aggregations'][b])

        res['collector'] = data['collector']
        if data.get('aggregations', {}).get('collector'):
            res['collector'].merge(data['aggregations']['collector'])

        # intel parsers
        res = parse_rec(data, res)
        if 'pme' in data:
            res = parse_pme(data, res)

        if 'cpe' not in res:  # create an empty pme for 2, 5 & cpe if there is no pme
            res['cpe'] = {}
        for index in ['2', '5', 'cpe']:  # this will delete old pmes
            if not res[index].get('pme', False):
                res[index]['pme'] = {
                    'all': [],
                    'total': 0,
                    'detail': {},
                    'ts': time.time(),
                }

        # handle geo location sent as None. If sent to ELK, it will break the indexing
        if data.get('metadata'):
            if data['metadata'].get('location', {}):
                if not data['metadata']['location'].get('latitude') or not data[
                    'metadata'
                ]['location'].get('longitude'):
                    del data['metadata']['location']
            res['metadata'] = data['metadata']

        valid_keys = [
            'nr',  # debug helper on replayed data, so that we can match for setting breaks
            'id',
            'ts',
            'conf',
            'WiFi',
            'DeviceInfo',
            'Hosts',
            'Ethernet',
            'PCP',
            'IP',
            'cache',
            'score',
            'forced_actions',
            'BulkData',
            'LocalAgent',
            'job',
            'tmp',  # store some temporary data like forced_actions. Wont go to the dbs
        ]
        for key in valid_keys:
            if data.get(key):
                res[key] = data[key]

        if data.get('rates'):
            res.merge(data['rates'])
        return res


def run():
    return run_app(partial(red.connect, WiFiFunctions))


if __name__ == '__main__':
    run()
