#!/usr/bin/env python
"""
wifi-test-socket-client

Creates test traffic to the socket server.
"""
from __future__ import print_function

import sys, os

sp = os.environ.get('sys_path_append')
if sp:
    sys.path.append(sp)
import socket
import time
from devapp.app import dirs, run_app, flag, FLG, app
from wifi.client.assets.sample_data import vf2

from wifi.client.axtract_sender import AxWifiSender as Sender


flag.string(
    'test_data',
    'vf2',
    'Module name in assets.sample_data or a python filename, defining "sample" globally.',
    short_name='s',
)
flag.string('host', '127.0.0.1', 'Server ip listening for readings.')
flag.integer('port', 16000, 'Server port.', short_name='p')
flag.integer('loops', 1, 'Loops')
flag.integer('dt', 1, 'Sleep between loops [millis]')
flag.bool(
    'assign_current_ts',
    True,
    'Assign current time into ts timestamp fields',
    short_name='c',
)
flag.enum(
    'msg_fmt', 'json', ['msgpack', 'str', 'json'], 'Packet format from the sender',
)


class ev:
    class cpe:
        cpeid = 'testcpe'


def load():
    exists = os.path.exists
    m = FLG.test_data
    here = os.path.abspath(__file__).rsplit('/', 1)[0]
    f = here + '/assets/sample_data/%s.py' % m
    if exists(f):
        m = f
    if not exists(m):
        app.die('Not found', datamod=m)
    d = {}
    with open(m) as fd:
        f = exec(fd.read(), d)
    if not 'sample' in d:
        app.die('Format error - require sample = {...}', datamod=m)
    return d['sample']


def start():
    sample = load()
    t0 = time.time()
    s = Sender(
        'sender', {'host': FLG.host, 'port': FLG.port, 'msg_fmt': FLG.msg_fmt}, {},
    )
    dt = FLG.dt / 1000.0

    for i in range(FLG.loops):
        # time.sleep(0.1)
        sample['id'] = str(i)
        sample['DeviceInfo']['SerialNumber'] = str(i)
        ev.props = sample
        ev.cpe.cpeid = sample['id']
        if FLG.dt > 99:
            print('sending', i)
        if FLG.assign_current_ts:
            sample['ts'] = int(round(time.time() * 1000))
        # seconds? then to millis:
        if sample['ts'] < 2000000000:
            sample['ts'] = sample['ts'] * 1000
        s.process_event(ev)
        time.sleep(dt)

    print('Sent %s readings in %ssecs' % (FLG.loops, time.time() - t0))


if __name__ == '__main__':
    run_app(start)
#
