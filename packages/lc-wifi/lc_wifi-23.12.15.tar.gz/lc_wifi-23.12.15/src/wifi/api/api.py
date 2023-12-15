from operators.con import con
from devapp.tools import FLG, time, now
from wifi.core.enforce import lookup


def api_activity_key(id):
    return f'api_active::{id}'


def job_timeout(typ):
    return getattr(FLG, f'job_{typ}_timeout', 200)


class api2:
    jobs = {
        'reboot': lambda args: {'Reboot': 'Reboot via AXWIFI'},
        'reconfigure': lambda args: {'MappedSetParameterValues': args},
        'factory_reset': lambda args: {'FactoryReset': 'Factory Reset via AXWIFI'},
    }

    @classmethod
    def chk(api2, _, __, *a, state_root, **kw):
        # state root is the msg, passed by pycond
        no_double_job = False, '-'
        msg = state_root
        pl = msg['payload']
        id = pl['params']['id']
        if pl['params'].get('author') == 'tester':
            return no_double_job
        con.redis.set({'active': True}, {}, api_activity_key(id), ex=200)  # FIXME
        evts = api2.read_redis_events(pl['params'], msg)['events']
        evts = [
            e
            for e in evts
            if e[1]['evt'].get('path') == '/finish' or e[1]['evt'].get('type')
        ]
        if not evts:
            return no_double_job
        if not evts[0]:
            return no_double_job
        ts, evt = evts[0]
        evt = evt['evt']
        if evt.get('path') == '/finish':
            return no_double_job
        types = [e for e in evts if e[1]['evt'].get('type')]
        if not types:
            return no_double_job
        job = types[0][1]['evt']
        try:
            timeout = job['ts'] + job.get('job_expiry', job_timeout(job.get('type')))
        except Exception:
            return no_double_job
        timeout = int(timeout - time.time())

        if timeout < 0:
            return no_double_job
        err = {'type': 'duplicate_job'}
        err['ui_title'] = 'Duplicate Job ⌛'
        user = job.get('params', {}).get('author', 'unknown')
        emsg = f'{job["type"]} job running from user {user}, timing out in {timeout} seconds.'
        err['ui_msg'] = emsg
        err['details'] = job
        msg['payload']['error'] = err
        msg['status_code'] = err['status_code'] = 405
        return True, '_'

    def update_redis(data, msg):
        # CAUTION: overwritten in poc
        p = data.get('body') or data
        try:
            p['result']['msg'] = p['result']['msg'].capitalize()
        except Exception:
            pass
        id = p['id']
        if 'type' in data:
            p['job_expiry'] = job_timeout(data['type'])
        con.redis.set_events({'evt': p}, msg=msg, key=f'apijob:{id}')

    def read_redis_events(data, msg):
        """Read from redis the events, (incl) from a ts given.
        When ts is not given or 0 we return all"""
        min = int(data.get('read_from', 0))
        if not min:
            min = '-'
        id = data['id']
        frm = data.get('discard_from')
        f = con.redis.get_events(
            data, msg, key=f'apijob:{id}', read_from=min, discard_from=frm
        )
        return {'events': f}

    @classmethod
    def prepare_kafka_job(cls, data, msg, job=None, job_type=None):
        job_type = data['path'][1:]
        id = data['params']['id']
        r = {'type': job_type, 'ts': time.time(), 'id': id}
        if job_type in {'optimize', 'refresh'}:
            r['params'] = data['params']
        else:
            r['job'] = {
                'steps': {'1': cls.jobs[job_type](data['params'].get('args') or {})}
            }
        job_id = data.get('job_id')
        if job_id:
            r['job_id'] = job_id
        return r

    def add_adhoc_enforce(data, adhoc):
        c2 = data.get('2', {}).get('expert', {}).get('cur_radio_ch')
        c5 = data.get('5', {}).get('expert', {}).get('cur_radio_ch')
        t2 = data.get('2', {}).get('expert', {}).get('target_radio_ch')
        t5 = data.get('5', {}).get('expert', {}).get('target_radio_ch')
        q2 = data.get('2', {}).get('expert', {}).get('target_q', 0)
        q5 = data.get('5', {}).get('expert', {}).get('target_q', 0)
        w = adhoc['params']['min_qual']
        w2, w5 = w.get('2', 2), w.get('5', 2)
        # keep target channels to be sent in the response
        b2 = None
        if q2 >= w2 and c2 != t2:
            lookup.add_enforce_2(data)
            b2 = data['2']['expert'].get('target_radio_ch')
        b5 = None
        if q5 >= w5 and c5 != t5:
            lookup.add_enforce_5(data)
            b5 = data['5']['expert'].get('target_radio_ch')
        return b2, b5

    @classmethod
    def qualify_adhoc(cls, data, msg):
        adhoc = data.get('metadata', {}).get('adhoc', {})
        is_usp = False
        if not adhoc:
            adhoc = data['collector'].get('job', {})
            is_usp = True
        _id = adhoc.get('id')
        tp = adhoc.get('type')
        if tp == 'optimize':
            # change type to enforce so that AXTRACT expects
            adhoc['type'] = 'enforce'
            b2, b5 = cls.add_adhoc_enforce(data, adhoc)
            # if is_usp: cls.send_usp_job(data)
            # data contains KPIs so needs to be stored kafka -> axt -> db
            if data.get('job'):
                data['aid'] = _id
                # keep target channels for response
                adhoc['enforce_2'] = b2
                adhoc['enforce_5'] = b5
        return data
