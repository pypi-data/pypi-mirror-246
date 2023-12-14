"""
USP Specific Functions
"""
import time
from ax.utils.ax_tree import AXTree
import requests
import json
from devapp.tools import get_deep, cast as simple_cast
from devapp.app import app
from absl import flags
from operators.con import add_connection, redis, con
from wifi.api import job_timeout, api_activity_key, api2
from time import sleep


flags.DEFINE_string(
    'axusp_api_endpoint',
    default='',
    help='RPC api endpoint to axiros controller',
)

# https://usp.technology/specification/index.htm#sec:use-of-authority-scheme-and-authority-id
usp_schemes = {
    'oui',
    'cid',
    'pen',
    'self',
    'user',
    'os',
    'ops',
    'uuid',
    'imei',
    'proto',
    'doc',
    'fqdn',
}

BULBS = {'connect': '🟩', 'promoted': '🟨', 'disconnect': '🟥'}


def is_usp_id(epid, _pref=usp_schemes):
    # FIXME: fix within flows ("Is USP" pycond) - use this function
    if epid.split(':', 1)[0] in _pref:
        return True


# leave this value str type when casting protobuf:
cast_leave = {'802.11'}


def cast(v, leave=cast_leave, c=simple_cast):
    """protobuf just delivers strings"""
    if v in cast_leave:
        return v
    try:
        return c(v)
    except Exception:
        return v


def cast_deep(m, cast=cast):
    r = AXTree({})
    for k, v in AXTree(m).iter_leaf_items():
        r[k] = cast(v)
    return r


def patched_update_redis(data, msg=None):
    msg = msg or {}
    p = data.get('body') or data
    p['ts'] = data.get('ts', time.time())
    id = p['id']
    if 'type' in data:
        p['job_expiry'] = data.get('ttl', job_timeout(data['type']))
        # data['type'] = data['type'].capitalize()
    try:
        m = p['result']['msg']
        m = m[0].upper() + m[1:]
        c = p['result']['code']
        if c > 299:
            m = f'❗{m}'
        p['result']['msg'] = m

    except Exception:
        pass
    if p.get('path') == '/progress':
        p['job_expiry'] = 0
    if p.get('path') == '/written':
        p['update_ui'] = True
        p['result']['msg'] = '💾 KPIs stored'
    elif p.get('path') == '/finish':
        if 'result' not in p:
            p['result'] = {'msg': 'forced finish', 'code': 200}
        if not is_usp_id(id):
            p['update_ui'] = True

    con.redis.set_events({'evt': p}, msg=msg, key=f'apijob:{id}')

    if p.get('path') == '/finish':
        time.sleep(0.001)
        api_start(id, '', '♾ Keep listening...', ttl=0)

    if p.get('path') == '/written':
        if is_usp_id(id):
            time.sleep(0.002)
            p['path'] = '/finish'
            p['result']['msg'] = '..'
            con.redis.set_events({'evt': p}, msg=msg, key=f'apijob:{id}')


def api_log_when_active(id, typ, data):
    if not con.redis.get({}, {}, key=api_activity_key(id)):
        return

    if typ == 'axwifi_realtime_valuechange':
        k, v = list(data['data'].items())[0]
        txt = f'{k[7:]}: {v}'
    else:
        txt = f'{typ} ({len(str(data))}B)'

    api_upd(id, f'⎆ {txt}')


def api_start(id, msg, type, ttl=100):
    return api2.update_redis({'type': type, 'ttl': 0, 'id': id})


def api_fin(id, msg, code=200):
    return api_upd(id, msg, code, path='/finish')


def api_upd(id, msg, code=200, path='/progress'):
    d = {
        'id': id,
        'path': path,
        'result': {
            'code': code,
            'msg': msg,
        },
    }
    api2.update_redis(d)


add_connection(redis.redis, 'axredis')


LightScanParams = [
    [
        'Device.BulkData.Profile.1.ReportingInterval',
        'Device.DeviceInfo.ProcessStatus.CPUUsage',
        'Device.DeviceInfo.ProductClass',
        'Device.DeviceInfo.SerialNumber',
        'Device.DeviceInfo.SoftwareVersion',
        'Device.DeviceInfo.UpTime',
        'Device.Hosts.Host.',
        'Device.WiFi.AccessPoint.',
        'Device.WiFi.Radio.',
        'Device.WiFi.SSID.',
        'Device.LocalAgent.Controller.',
        # 'Device.LocalAgent.Controller.1.MTP.*.Enable',
        # 'Device.LocalAgent.Controller.1.MTP.*.Protocol',
        'Device.DeviceInfo.HardwareVersion',
        'Device.DeviceInfo.Manufacturer',
        'Device.DeviceInfo.ManufacturerOUI',
        'Device.DeviceInfo.MemoryStatus.Free',
        'Device.DeviceInfo.MemoryStatus.Total',
        'Device.DeviceInfo.ModelName',
        'Device.Ethernet.Link.',
        'Device.IEEE1905.AL.NetworkTopology.',
    ],
    0,
]


def dt(t0):
    return int(1000 * (time.time() - t0))


class axiros_controller:
    """This is currently only one: The Axiros Controller"""

    HDR = {'Content-Type': 'application/json'}

    @classmethod
    def rpc(contr, jobd, data):
        patch = getattr(contr.vendor_patches, jobd['typ'], None)
        if patch:
            patch(jobd, data)
        b = json.dumps(jobd['body'])
        return requests.post(
            jobd['endpoint'], b, headers=contr.HDR, timeout=jobd['timeout']
        )


def is_avm(jobd, data):
    di = data.get('props')
    if di:
        return di['Device.DeviceInfo.Manufacturer']


class usp:
    """The usp function tree for NodeRed"""

    c_nb_by_epid = {}  # for multicontroller mode, filled from anywhere, e.g. at connect

    class controller(axiros_controller):
        class vendor_patches:
            def operate(jobd, data):
                if jobd['body']['command'] == 'Device.WiFi.NeighboringWiFiDiagnostic()':
                    if is_avm(jobd, data):
                        jobd['body']['args'] = [['X_AVM-DE_ForceRescan', 'true']]

    @classmethod
    def job(usp, data, msg=None, err_info=True):
        id = data.get('id') or data['epid']
        usp_job = data.get('usp_job', data)  # old format
        typ, body = usp_job['type'], usp_job['body']
        ep = usp.c_nb_by_epid.get(id) or flags.FLAGS.axusp_api_endpoint
        endpoint = ep + f'/v1/{id}/{typ}'
        timeout = usp_job.get('timeout', 5)
        t0 = time.time()
        jobd = {'timeout': timeout, 'endpoint': endpoint, 'typ': typ, 'body': body}
        try:
            # if typ == 'operate': breakpoint()  # FIXME BREAKPOINT
            res = usp.controller.rpc(jobd, data)
            r = res.text
            s = res.status_code
            l = len(r)  # noqa: E741
            txt = f'Status {s} {dt(t0)}ms {l}B'
            try:
                r = json.loads(r)
            except Exception:
                pass
        except Exception as ex:
            r = txt = str(ex)
            s = 500
        sleep(0.001)  # redis / UI
        if typ == 'operate':
            typ = f'{typ} {body["command"]}'
        txt = f'⚙️ /{typ.ljust(10)}: {txt}'
        api_upd(id, txt, s)

        data['resp_status'] = s
        data['resp'] = r
        try:
            res = r['Response']['GetResp']['req_path_results']
            m = {}

            def add(m, pth, params):
                n = {pth + k: params[k] for k in params}
                m.update(n)

            def jobd(k, m):
                for i in k['resolved_path_results']:
                    add(m, i['resolved_path'], i['result_params'])

            [jobd(k, m=m) for k in res]
            data['resp_dict'] = m
        except Exception:
            pass

    @classmethod
    def enforce(usp, data):
        id = data['id']
        j = None
        for d in data, data['collector']:
            try:
                j = d['job']['steps']['1']['MappedSetParameterValues']
                break
            except Exception:
                pass
        if not j:
            api_fin(id, 'No changes to be enforced')
            return {'a': 'b'}

        r = {}

        def add(node, leaf, v):
            h = r.setdefault(node + '.', [])
            h.append([leaf, str(v), True])

        j = {k: v for k, v in AXTree(j).iter_leaf_items()}
        m = {}
        new = {}
        for k, v in j.items():
            node, leaf = k.rsplit('.', 1)
            N = data.get(node)
            o = N.get('orig_' + leaf)
            if o:
                l = o.split(':')
                leaf = leafui = l.pop(0)
                for val_proc in l:
                    if val_proc == 'int':
                        v = int(v)

            leafui = leaf
            o = N.get('orig_node')
            if o:
                leafui = f'..{leaf}'
                node = o
            else:
                o = N.get('idx_orig')
                new[k] = v
                if o:
                    leafui = f'..{o}.{leaf}'
                    node = node.rsplit('.', 1)[0] + f'.{o}'
            m[leafui] = v
            v = str(v).replace('False', 'false').replace('True', 'true')
            add(node, leaf, v)

        if r:
            r = [[k, v] for k, v in r.items()]
            job = {
                'timeout': 20,  # jointelli...
                'type': 'set',
                'epid': id,
                'body': {
                    'allow_partial': True,
                    'update_objs': r,
                },
            }
            app.info('set job', json=r)
            usp.job(job, err_info=False)
            m = ' '.join([f'{k}:{v}' for k, v in m.items()])
            if 'oper_failure' in str(job):
                code = 400
                m = 'Failed ' + m
            else:
                code = 200
                m = f'✔️ {m}'
                data.update(new)
            api_fin(id, m, code=code)

    @classmethod
    def req_fullscan(usp, data, msg=None):
        return usp.req_operate(data, type='fullscan')

    class lightscan:
        # @classmethod
        # def get_res_to_bulk_fmt(ls, data):
        #     d = data['resp_dict']
        #     d['CollectionTime'] = int(time.time())
        #     epid = data['epid']
        #     cepid = 'proto::controller'
        #     r = to_bulk_fmt(cepid, epid, d)
        #     return r

        @classmethod
        def to_tr181(ls, data):
            """patched when we have non std ones"""
            return

        @classmethod
        def params_by_cpeid(ls, _):
            """patched when we have non std ones"""
            return LightScanParams

        @classmethod
        def get(ls, data):
            id = data['id']
            params = ls.params_by_cpeid(id)
            job = {'type': 'get', 'epid': id, 'body': params, 'timeout': 20}
            usp.job(job)
            r = job.get('resp_dict')
            if not r:
                api_fin(id, 'RPC failed with controller', code=400)
                raise Exception(f'RPC failed {r}')
            api_upd(id, 'Got WiFi state.')
            if 'interval' in data:
                r['Device.BulkData.Profile.1.ReportingInterval'] = data['interval']
            data['props'] = r

        @classmethod
        def to_redis(ls, data):
            id = data['id']
            key = f'light_scan::{id}'
            con.redis.set(data, {}, key, ex=200)  # FIXME
            return data

        @classmethod
        def from_redis(ls, data):
            id = data['id']
            key = f'light_scan::{id}'
            r = con.redis.get({}, {}, key)
            if not r:
                return app.warn('No lightscan data')
            data['lightscan'] = con.redis.get({}, {}, key)

    @classmethod
    def req_operate(usp, data, msg=None, type=None):
        id = data['id']
        # backward compat, then no vendor hooks will work
        type = type or data.get('type')
        if type == 'reboot':
            cmd = 'Device.Reboot()'
        elif type == 'factory_reset':
            cmd = 'Device.FactoryReset()'
        elif type in {'refresh', 'optimize', 'fullscan'}:
            cmd = 'Device.WiFi.NeighboringWiFiDiagnostic()'
        else:
            raise Exception('unsupported cmd')
        job = {
            'type': 'operate',
            'epid': id,
            'body': {
                'command': cmd,
                'command_key': f'{type}',
                'send_resp': True,
                'args': [],
            },
        }
        data['usp_job'] = job
        usp.job(data)

    class msg_fmt:
        def axwifi_realtime_valuechange(data, details):
            """
            "data": {
                  "param_path": "Device.Hosts.Host.1.WANStats.PacketsSent",
                  "param_value": "77955"
              },
              "epid": "epid",
              "type": "axwifi_realtime_valuechange"
            """
            d = details['value_change']
            k, v = d['param_path'], cast(str(d['param_value']))
            return {k: v}

        def fullscan(data, details):
            d = details['oper_complete']
            try:
                d = d.get('req_output_args')['output_args']
            except Exception:
                d = {'Status': 'Error', 'err': d.get('cmd_failure')}
            return d

        def lightscan(data, details):
            d = details['event']['params']['Data']
            return json.loads(d) if isinstance(d, str) else d

        unknown = 'unknown'
        val_change = 'val_change'

    @classmethod
    def qualify_msg(usp, data: dict, msg: dict):
        """All leave with 'type', 'id', 'data'"""
        epid = 'unknown_epid'
        try:
            data = data['data']['payload']
            epid = data['epid']
            if 'details' not in data:
                typ = data.get('type', 'skip')
                if typ in ('connect', 'promoted', 'disconnect'):
                    status = BULBS[typ]
                    api_upd(epid, f'{status} CPE {typ}')
                    data = {'data': data}
                    data['type'] = typ
                else:
                    data['type'] = 'skip'
                    app.info('discarding', payload=data)
            else:
                det = data['details']
                typ = det['subscription_id']
                if typ == 'axwifi_realtime_operationcomplete':
                    cmd_key = det['oper_complete']['command_key']
                    if cmd_key in {'refresh', 'optimize', 'fullscan'}:
                        typ = 'fullscan'
                elif typ == 'axwifi_push':
                    typ = 'lightscan'
                elif typ == 'axwifi_realtime_events':
                    event = det['event']
                    prms = event.get('params', {})
                    event_name = event.get('event_name', {})
                    cause = prms.get('Cause', '').lower()
                    if 'Boot!' in event_name:
                        typ = 'factory_reset' if 'factory' in cause else 'boot'
                    # no job over reboots
                    api_fin(epid, '🔛 CPE up again')

                fmt = getattr(usp.msg_fmt, typ, '')
                if fmt:
                    data = {'data': fmt(data, det)}
                else:
                    data = {'data': det}
                api_log_when_active(epid, typ, data)
                data['type'] = typ
        except Exception as prms:
            raise
        data['id'] = data['z'] = epid  # e.g. for log
        data['log'] = []
        app.info(data['type'], cpe=epid)
        return data

    @classmethod
    def to_datamodel(usp, data, msg):
        """we have either lightscan only, ls with fs or fs"""
        job = None
        fullsc = None
        cast_ = False
        props = None

        if data['type'] == 'reconfigure':
            cast_ = True
            props = data['props']
            job = data.pop('job')
            job['type'] = 'reconfigure'

        elif data['type'] in {'refresh', 'lightscan.get'}:
            # light = true
            props = data['props']
            cast_ = True

        elif data['type'] == 'lightscan':
            props = data.pop('data')['Report'][0]

        elif data['type'] == 'fullscan':
            fullsc = data.pop('data')
            ls = data.pop('lightscan')
            rep = ls.get('data', {}).get('Report')
            if rep:
                props = rep[0]
            else:
                props = ls.pop('props')
                cast_ = True
                # from redis:
                job = ls

        if not props:
            breakpoint()  # FIXME BREAKPOINT
        if cast_:
            props = {
                k: cast(v) for k, v in props.items() if not k.endswith('InterfaceType')
            }
        usp.normalize_lightscan_from_bulk(props, into=data)
        if job:
            data['props']['collector']['job'] = job
        r = {
            'ts': int(time.time() * 1000),
            'cpeid': data['id'],
            'sender': {
                'name': 'axusp_collector',
            },
        }
        data.update(r)
        if not fullsc:
            return data
        if fullsc['Status'] in ['Complete', 'Success'] and 'Result' in fullsc:
            usp.normalize_fullscan(fullsc, into=data)
            dt = int(1000 * (time.time() - msg['ts']))
            data['props']['WiFi']['NeighboringWiFiDiagnostic']['scan_dt'] = dt
            data['type'] = 'fullscan_norm'
            fsm = {'light_scan': 0, 'full_scan': 1, 'msg': 'Full Scan'}
            data['props']['collector'].update(fsm)
        else:
            try:
                txt = fullsc['err']['err_msg']
                txt = f'CPE reports: "{txt}"'
            except Exception:
                txt = 'Missing scan data'
            api_upd(data['id'], txt, 305)

    def normalize_lightscan_from_bulk(props, into):
        into['ts'] = props.pop('CollectionTime', time.time())
        props = AXTree(props)
        into['props'] = p = props.pop('Device')
        p['collector'] = {
            'msg': 'Light Scan',
            'full_scan': 0,
            'code': 200,
            'details': '',
            'light_scan': 1,
        }
        into['type'] = 'lightscan_norm'

    def normalize_fullscan(data, into):
        d = AXTree(data)
        into['props']['WiFi']['NeighboringWiFiDiagnostic'] = d
        d['DiagnosticsState'] = d['Status']
        d['ResultNumberOfEntries'] = len(d['Result'])

    def normalize_tr181_indexes(data):
        """AXW Convention: All indizes (and refs) are 1-4 for 2 Ghz stuff
        and 5- ... for 5Ghz
        """
        t0 = time.time()
        props = data['props'].get('WiFi')
        if not props:
            return
        # e.g. replrad = {'Device.WiFi.Radio.2': 'Device.WiFi.Radio.5'}
        changed_radio_idxs = rearrange_idx_for_2_and_5(props, 'Radio', is2=radio_is_2ghz)
        for k in [
            ['SSID', 'LowerLayers'],
            ['NeighboringWiFiDiagnostic.Result', 'Radio'],
        ]:
            replace_refs_and_create_virtual_objs(props, k, changed_radio_idxs)

        changed_ssid_idxs = rearrange_idx_for_2_and_5(props, 'SSID', is2=low_lay_is_2ghz)
        replace_refs_and_create_virtual_objs(
            props, ['AccessPoint', 'SSIDReference'], changed_ssid_idxs
        )
        changed_api_idxs = rearrange_idx_for_2_and_5(
            props, 'AccessPoint', is2=ssid_ref_is_2ghz
        )
        app.info(
            'Normalized',
            dt=time.time() - t0,
            json={
                'radios': changed_radio_idxs,
                'ssids': changed_ssid_idxs,
                'aps': changed_api_idxs,
            },
        )

    def fake_hosts_active(data):
        # when no devicde is connected....
        h = data['props'].get('Hosts', {}).get('Host', {})
        for k, v in h.items():
            v['Active'] = True
            if k == '1':
                v['Active'] = 1


def radio_is_2ghz(r):
    return '5' not in r['OperatingFrequencyBand']


def ref_is_2ghz(r, ref):
    # rearranged lower layers already:
    return int(r[ref].rsplit('.', 1)[-1]) < 5


def low_lay_is_2ghz(r):
    return ref_is_2ghz(r, 'LowerLayers')


def ssid_ref_is_2ghz(r):
    return ref_is_2ghz(r, 'SSIDReference')


def replace_refs_and_create_virtual_objs(props, key, repl):
    if not repl:
        return
    o = get_deep(key[0], props, dflt=0)
    if not o:
        return

    # o has v e.g. like {'BSSID': '62:ED:6F:76:FD:97', 'LowerLayers': 'Device.WiFi.Radio.1,Device.WiFi.Radio.2'}
    # -> we find those multis and return them in a 'new' dict of artificial objects, with just a single ref
    new = {}
    do_single_repl_ref(o, key[1], repl, new=new)
    if new:
        do_single_repl_ref(new, key[1], repl, new)
        o.update(new)


def do_single_repl_ref(o, key, repl, new):
    for k in o:
        v = o[k]
        if key not in v.keys():
            continue
        old = v[key]
        if ',' not in old:
            n = repl.get(old, old)
            if not isinstance(n, list):
                v[key] = n
                continue
            multi = n
            v[key] = n[0]
        else:
            multi = [i.strip() for i in old.split(',')]
            v[key] = repl.get(multi[0], multi[0])
        for r in multi[1:]:
            nd = dict(v)
            nd['idx_virt'] = k
            nd[key] = repl.get(r, r)
            # find idx to insert the new artificial obj
            idx = len(o) + len(new) + 1  # idx start at 1
            while str(idx) in o or str(idx) in new:
                idx += 1
            new[str(idx)] = nd


def rearrange_idx_for_2_and_5(props, pth, is2, i2=0, i5=4):
    """Our convention was: all 2Ghz idxs are 1,2,.. and 5Ghzs ones 5,6...
    Do this here, but keep the original idx for later jobs:
    """
    repl = {}
    r = {}

    obj = props.get(pth)
    if not obj:
        return r
    for k, v in sorted(obj.items()):
        idx_orig = v.get('idx_virt', k)
        ref = f'Device.WiFi.{pth}.{idx_orig}'
        if is2(v):
            i2 += 1
            i = i2
        else:
            i5 += 1
            i = i5
        nref = f'Device.WiFi.{pth}.{i}'
        r[str(i)] = v
        v['idx_orig'] = idx_orig
        if nref != ref:
            v = repl.get(ref)
            if v:
                repl[ref] = v if isinstance(v, list) else [v]
                repl[ref].append(nref)
            else:
                repl[ref] = nref
    props[pth] = r
    return repl


# c = Functions.usp
# add_pre_post_hook(c, 'to_datamodel', fix_avm_lower_layers_end_dot)
#
# def add_pre_post_hook(cls, orig_func_name, hook, mode='pre'):
#     orig = getattr(cls, orig_func_name)
#     if mode == 'pre':
#
#         def h(data, msg=None, **kw):
#             data = hook(data, msg, **kw) or
#             return orig(hook(*a, **kw))
#
#     else:
#
#         def h(*a, **kw):
#             return hook(orig(*a, **kw))
#
#     setattr(cls, orig_func_name, h)

orig = usp.to_datamodel


def fix_avm_lower_layers_end_dot(data, msg=None, orig=orig):
    # some lower layer refs hava a dot at the end (only AVM)
    try:
        if 'props' in data:
            collection = data['props']
        else:
            collection = data['lightscan']['data']['Report'][0]
    except Exception:
        return orig(data, msg)

    def fix(v):
        # avm guest nw: 'Device.WiFi.SSID.3.LowerLayers': 'Device.WiFi.Radio.1.,Device.WiFi.Radio.2'}
        if ',' in v:
            return ','.join([fix(i.strip()) for i in v.split(',')])
        return v[:-1] if v[-1] == '.' else v

    lls = {k: fix(collection[k]) for k in collection if k.endswith('.LowerLayers')}
    collection.update(lls)
    return orig(data, msg)


usp.to_datamodel = fix_avm_lower_layers_end_dot


# TODO put this all into product
api2.update_redis = patched_update_redis
api2.api_log_when_active = api_log_when_active
api2.api_start = api_start
api2.api_fin = api_fin
api2.api_upd = api_upd
# _.send_usp_job = Functions.usp.send_usp_job
