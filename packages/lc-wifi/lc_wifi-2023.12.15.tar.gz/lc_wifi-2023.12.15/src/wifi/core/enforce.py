from devapp.tools import deep_update, define_flags, time
from operators.con import con

now = time.time


class flags:
    autoshort = 'w'

    class job_reboot_timeout:
        d = 180

    class job_reconfigure_timeout:
        d = 30

    class job_factory_reset_timeout:
        d = 180

    class job_optimize_timeout:
        d = 120

    class job_refresh_timeout:
        d = 90


define_flags(flags)


def enforce(data, b):
    t_ch = data[b]['expert']['target_radio_ch']
    t_bw_raw = data[b]['expert']['target_bw']
    t_bw = t_bw_raw if t_bw_raw == 'Auto' else str(t_bw_raw) + 'MHz'
    p = 'WiFi.Radio.%s.' % ('1' if b == '2' else '5')
    m = {
        p + 'Channel': t_ch,
        p + 'AutoChannelEnable': 0,
        p + 'OperatingChannelBandwidth': t_bw,
    }
    deep_update(
        data,
        {
            b: {'expert': {'denied_by_condition': False}},
            'cache': {b: {'last_enf_ts': now(), 'last_enf_ch': t_ch}},
            'job': {'steps': {'1': {'MappedSetParameterValues': m}}},
        },
    )
    return True


def rollback(data, b):
    p = 'WiFi.Radio.%s.' % ('1' if b == '2' else '5')
    m = {
        p + 'AutoChannelEnable': 1,
    }
    deep_update(data, {'job': {'steps': {'1': {'MappedSetParameterValues': m}}}})
    return True


def mapped_spv(data, args):
    deep_update(data, {'job': {'steps': {'1': {'MappedSetParameterValues': args}}}})
    return True


def reboot(data):
    deep_update(data, {'job': {'steps': {'1': {'Reboot': 'Reboot via AXWIFI'}}}})
    return True


def factory_reset(data):
    deep_update(
        data,
        {'job': {'steps': {'1': {'FactoryReset': 'Factory Reset via AXWIFI'}}}},
    )
    return True


evt_key = 'qualities:{d[id]}'  # redis


def forced_actions(data, **kw):
    FORCE_REBOOT = FORCE_OPTIMIZE_2 = FORCE_OPTIMIZE_5 = False
    forced_reboot = forced_optimize_2 = forced_optimize_5 = 0  # for elk
    data['forced_actions'] = []
    if 'tmp' not in data:
        data['tmp'] = {}

    # check PME and see if there is any Forced actions requested
    for k, v in data.get('pme', {}).items():
        if k == 'ts':
            continue
        for item in v:
            if item.get('enforce', False) and item.get('action', None):
                this_action = f"{item['action']}_{k}"
                if this_action.startswith('reboot'):
                    FORCE_REBOOT = True
                elif this_action == 'optimize_2':
                    FORCE_OPTIMIZE_2 = True
                elif this_action == 'optimize_5':
                    FORCE_OPTIMIZE_5 = True

    config = kw.get('config', {}).get('delay_between_forced_in_s')

    # now lets do the forced reboot or optimize IF needed
    # TODO: move the repeating code to a function in below 3 ifs
    _one_day_in_s = 60 * 60 * 24
    if FORCE_REBOOT:
        _now = time.time()
        _delay_between = config.get('reboot', _one_day_in_s)
        for ts, events in data.get('history', {}).get('events', []):
            for ts, action in events.get('forced_actions', []):
                if ts > _now - _delay_between and action.startswith('reboot'):
                    FORCE_REBOOT = False
                    break
            if not FORCE_REBOOT:
                break  # do not continue checking past events if you already had a case
        if FORCE_REBOOT:  # none of the history is in recept day
            data['forced_actions'].append((time.time(), 'reboot'))
            from wifi.api import api2

            d = {
                'id': data['id'],
                'path': '/pme_reboot',
                'ttl': 60,
                'result': {
                    'code': 200,
                    'msg': 'PME requested a Reboot',
                },
            }
            api2.update_redis(d)
            forced_reboot += 1
            reboot(data)
    if FORCE_OPTIMIZE_2:
        _now = time.time()
        _delay_between = config.get('optimize', _one_day_in_s)
        for ts, events in data.get('history', {}).get('events', []):
            for ts, action in events.get('forced_actions', []):
                if ts > _now - _delay_between and action == 'optimize_2':
                    FORCE_OPTIMIZE_2 = False
                    break
            if not FORCE_OPTIMIZE_2:
                break  # do not continue checking past events if you already had a case
        if FORCE_OPTIMIZE_2:  # none of the history is in recept day
            data['forced_actions'].append((time.time(), 'optimize_2'))
            data['tmp']['forced_actions_2'] = True
            from wifi.api import api2

            d = {
                'id': data['id'],
                'path': '/pme_optimize',
                'ttl': 60,
                'result': {
                    'code': 200,
                    'msg': 'PME requested optimization on 2.4Ghz',
                },
            }
            api2.update_redis(d)
            forced_optimize_2 += 1

    if FORCE_OPTIMIZE_5:
        _now = time.time()
        _delay_between = config.get('optimize', _one_day_in_s)
        for ts, events in data.get('history', {}).get('events', []):
            for ts, action in events.get('forced_actions', []):
                if ts > _now - _delay_between and action == 'optimize_5':
                    FORCE_OPTIMIZE_5 = False
                    break
            if not FORCE_OPTIMIZE_5:
                break  # do not continue checking past events if you already had a case
        if FORCE_OPTIMIZE_5:  # none of the history is in recept day
            data['forced_actions'].append((time.time(), 'optimize_5'))
            data['tmp']['forced_actions_5'] = True
            from wifi.api import api2

            d = {
                'id': data['id'],
                'path': '/pme_optimize',
                'ttl': 60,
                'result': {
                    'code': 200,
                    'msg': 'PME requested optimization on 5Ghz',
                },
            }
            api2.update_redis(d)
            forced_optimize_5 += 1
    data['tmp']['forced_reboot'] = forced_reboot
    data['tmp']['forced_optimize_2'] = forced_optimize_2
    data['tmp']['forced_optimize_5'] = forced_optimize_5
    return data


class lookup:
    def history(k, v, cfg, data, count=None, **kw):
        """loading redis history async (only when other improve conditions are met)"""
        con.redis.get_events(data, msg=None, key=evt_key, pth='history', count=count)
        hist = data.pop('history', {}).get('events')
        if hist:
            # add your crits here - you have the last <count> events
            pass
            # print('hist', hist)
        return True, 0

    def add_enforce_2(data, **_):
        return enforce(data, '2')

    def add_enforce_5(data, **_):
        return enforce(data, '5')

    def add_rollback_2(data, **_):
        return rollback(data, '2')

    def add_rollback_5(data, **_):
        return rollback(data, '5')
