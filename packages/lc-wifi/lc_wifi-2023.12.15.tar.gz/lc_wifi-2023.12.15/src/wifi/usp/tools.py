from wifi.usp import usp
from devapp.app import app
from devapp.tools import write_file, json, time
from ax.utils import ax_tree


def explore_fn(di):
    k = [
        'ManufacturerOUI',
        'ModelName',
        'HardwareVersion',
        'SoftwareVersion',
    ]
    r = [di.get(v, '') for v in k]
    return './data/explore/explore_%s.json' % '_._'.join(r)


# def to_bulk_fmt(cepid, epid, d):
#     det = {
#         'event': {
#             'event_name': 'Push!',
#             'obj_path': 'Device.BulkData.Profile.1',
#             'params': {'Data': {'Report': [d]}},
#         },
#         'send_resp': True,
#         'subscription_id': 'axwifi_push',
#     }
#     return {
#         'final': 0,
#         'session_id': '',
#         'data': {
#             'payload': {
#                 'c_epid': cepid,
#                 'epid': epid,
#                 'list_type': 'authenticated',
#                 'type': 'notify',
#                 'details': det,
#             }
#         },
#     }


class tools:
    @classmethod
    def _get(tools, epid, pth, lvl=0):
        app.info('device get', pth=pth, epid=epid)
        pths = [pth] if isinstance(pth, str) else pth
        j = {'type': 'get', 'epid': epid, 'body': [pths, lvl]}
        usp.job(j)
        if not 'resp_dict' in j:
            return app.error('No get result', job=j)
        d = j['resp_dict']
        d.pop('Device.DeviceInfo.DeviceLog', 0)
        return d

    @classmethod
    def explore(tools, data, hir=0, R=None):
        """a first level only somewhat safe recursive way of exploring what the device can do."""
        if isinstance(data, str):
            path = ['Device.']
            epid = data
        else:
            epid, path = data['epid'], data['paths']
        if hir == 0:
            R = {'cmds': {}, 'evts': {}, 'params': {}}
            res = tools._get(epid, 'Device.DeviceInfo.', lvl=1)
            if not res:
                return
            R['di'] = {k.rsplit('.', 1)[-1]: v for k, v in res.items()}
        app.info('exploring', path=path[0], params=len(R['params']))

        d = {
            'type': 'getsupporteddm',
            'epid': epid,
            'body': {
                'first_level_only': True,
                'return_commands': True,
                'return_events': True,
                'return_params': True,
                'paths': path,
            },
        }
        # device sometimes needs time to reorg (jointelly poc)
        for i in range(3):
            usp.job(d)
            resp = d.get('resp')
            if resp:
                break
            app.warn('retrying after 2s [%s/3]' % (i + 1), path=path[0])
            time.sleep(2.0)
        if not resp:
            app.info('No resp - stopping explore', json=d, path=path)
            return
        objs = resp['Response']['GetSupportedDMResp']['req_obj_results'][0]
        objs = objs.get('supported_objs')

        def do_param(p, epid=epid, pth=path[0]):
            t = p.get('value_type', 'str').lower()
            l = ['str', 'int', 'long', 'bool', 'float']
            for k in l:
                if k in t:
                    return k
            return t

        for p in objs:
            for s, k in [
                ['cmds', 'supported_commands'],
                ['evts', 'supported_events'],
            ]:
                if k in p:
                    R[s][path[0]] = p[k]
            sub = p.get('supported_obj_path')
            if sub and not [sub] == path:
                tools.explore({'epid': epid, 'paths': [sub]}, hir + 1, R)
            params_ = p.get('supported_params')
            if params_:
                R['params'].update(
                    {path[0] + p['param_name']: do_param(p) for p in params_}
                )
        if hir == 0:
            fn = explore_fn(R['di'])
            write_file(fn, json.dumps(R, indent=4), mkdir=1, log=1)

        return R

    @classmethod
    def get_all(tools, data):
        if isinstance(data, str):
            epid = data
        else:
            epid = data['epid']

        breakpoint()  # FIXME BREAKPOINT
        di = tools._get(epid, 'Device.DeviceInfo.', 1)
        expl = read_file(explore_fn(di))
        breakpoint()  # FIXME BREAKPOINT

    def get_res_to_dict(data):
        """Parse a USP get result into a dict"""
        R = data['Response']
        R = R['GetResp']['req_path_results']
        R = R[0]['resolved_path_results']
        r = {}

        for p in R:
            pth = p['resolved_path']
            for k, v in p['result_params'].items():
                r[pth + k] = v
        return r
