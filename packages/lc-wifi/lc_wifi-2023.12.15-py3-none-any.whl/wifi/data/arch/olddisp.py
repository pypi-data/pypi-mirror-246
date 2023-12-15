#!/usr/bin/env python
"""
Dispatcher of on-socket events to a http hub. Can also forward events to
other socket server, low level.

"""
from __future__ import print_function

from gevent import monkey

monkey.patch_all()

import os
import rx
import sys
import uuid
import time
import socket
import urllib3
import lz4.frame
import ujson as json
from gevent.server import StreamServer
from requests import post, get, Session
from devapp.app import dirs, run_app, flag, FLG, app
from streampipes.remote_publish import remote_publish
from streampipes.common import U8, err, here, host_port, now, op
from wifi.misc_util import err_exit, pass_, ldd, U8, to_url, tn

GS = rx.concurrency.mainloopscheduler.GEventScheduler()
O = rx.Observable
flag.boolean('debug', False, 'Debugmode')
flag.boolean('per_sock_stats', True, 'Per socket stats per interval')
flag.string('bind', '16000', 'Bind ip:port to listen for data.')
flag.string('realm', 'AX.test.lab', 'Hierarchical realm')
flag.string('token', '', 'Token valid for the realm')
flag.alias('port', 'bind')
flag.string(
    'echo_socket',
    '',
    'IP:Port to echo received data to - for daisy chaining dispatchers.',
)
flag.integer('stats_int', 10000, 'Logging stats in that interval (millis)')
flag.enum('msg_fmt', 'json', ['str', 'json'], 'Packet format from the sender')

now = lambda: int(time.time() * 1000)
data_in = rx.subjects.Subject()
lines_in = rx.subjects.Subject()

stats = {
    'data': 0,
    'err_decode': 0,
    'server_connects': 0,
    'err_server': 0,
    'batches': 0,
    'dt': {},
    'sockets': 0,
}


echo_socks = {}


def echo_sender_stream():
    if not ':' in FLG.echo_socket:
        FLG.echo_socket = '127.0.0.1:%s' % FLG.echo_socket
    h, p = FLG.echo_socket.split(':')
    if '%s:%s' % (h, p) == '%s:%s' % (FLG.bind, FLG.port):
        app.log.error('Echo sendto bind == our own socket. Yeah sure. Refused.')
        sys.exit(1)
    p = int(p)

    def sock(h=h, p=p):
        # Create a TCP/IP socket
        sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        sock_.connect((h, p))
        return sock_

    def echo_lines(l, bls=b'\n'):
        frm, line = l
        m = echo_socks.get(frm)  # set by the handler
        if m is None:
            # closed
            return l
        try:
            s = m.get('sock')
            if not s:
                s = m['sock'] = sock()
            while True:
                ret = s.send(line)
                if ret == 0:
                    break
                line = line[ret:]

        except Exception as exc:
            app.log.error('Could not connect to echo socket', exc=exc)
            time.sleep(3)
            m['sock'] = None
        return l

    return lines_in.observe_on(GS).map(echo_lines)


# this handler will be run for each incoming connection in a dedicated greenlet
def receive_line_sep(socket, address):
    # socket.sendall(b'Welcome to the echo server! Type quit to exit.\r\n')
    # using a makefile because we want to use readline()
    rfileobj = socket.makefile(mode='rb')
    addr = '%s:%s' % (address[0], address[1])
    stats['sockets'] += 1
    if FLG.echo_socket:
        echo_socks[addr] = {}
    echo = bool(FLG.echo_socket)
    while True:
        line = rfileobj.readline()
        if echo:
            lines_in.on_next((addr, line))
            time.sleep(0)
        line = line.strip()
        if not line:
            break
        s = stats['dt'].get(addr)
        if not s:
            stats['dt'][addr] = s = [0, 0]

        try:
            v = eval(line) if FLG.msg_fmt == 'str' else json.loads(line)
            if not 'id' in v:
                continue
        except Exception as ex:
            stats['err_decode'] += 1
            s[1] += 1
            continue

        if line.strip().lower() == b'quit':
            break
        # socket.sendall(line)
        stats['data'] += 1
        s[0] += 1
        m = v.setdefault('sender', {})
        m['addr'] = addr
        v['ts'] = v.get('ts') or now()
        data_in.on_next(v)
    rfileobj.close()
    echo_socks.pop(addr, 0)


# --------------------------------------------------------------- Cloud Adapter
flag.boolean('server_verify_ssl', True, 'Server check SSL')
flag.integer('server_buffer_max_secs', 1, 'Server buffer max seconds')
flag.integer('server_buffer_max_items', 1000, 'Server buffer max items')
flag.integer('server_port', 443, 'Server port for replacement in server url')

flag.string('proc_id', '<hostname>.<port>.<pid>', 'Process identifier of socket server')
flag.string(
    'server_url',
    'https://axc2.axiros.com:<server_port>/wifi/2/api/<realm>/<proc_id>/data',
    'If server mode then send data to this AXWiFi cloud server URL',
)

flag.enum(
    'data_conf_regulatory_domain',
    'ETSI',
    ['ETSI', 'FCC', 'JAPAN'],
    'Dictating allowed channel ranges',
)

flag.integer('data_conf_upper_chan_2', 0, '0: auto, based on reg.domain.')
flag.float(
    'data_conf_dfs_weight', 0.9, 'Weight factor for DFS. Set to 0 to exclude DFS',
)

flag.enum(
    'data_conf_algo_2',
    'base',
    ['base', 'odiac'],
    'Algorithm type selector for 2.4GHz band',
)

loads, dumps = json.loads, json.dumps
session = None
stream_id = None
base_url = None


def add_meta_data(rs):
    # TODO: keep the rx3 listiterator!
    id = str(uuid.uuid4())
    r = {
        'stream': 'AX.WiFi.stream.readings',
        'data': rs,
        'sender': {
            'name': 'socketserver',
            'data_id': id,
            'stream_id': stream_id,
            'realm': FLG.realm,
            'proc_id': PROC_ID,
            'hostname': HOSTNAME,
            'pid': os.getpid(),
            'ts': now(),
            'add_data': data_flags,
        },
    }
    return r


PROC_ID = None
PID = os.getpid()
HOSTNAME = socket.gethostname()


def cloud_sender_stream():
    global base_url, PROC_ID
    # replacements
    m = {
        'server_port': FLG.server_port,
        'hostname': HOSTNAME,
        'realm': FLG.realm,
        'port': FLG.port,
        'pid': PID,
    }
    proc_id = FLG.proc_id
    for k, v in m.items():
        proc_id = proc_id.replace('<%s>' % k, str(v))
    m['proc_id'] = PROC_ID = proc_id
    app.log.debug('Process properties', **m)
    bu = to_url(FLG.server_url)
    for k, v in m.items():
        bu = bu.replace('<%s>' % k, str(v))
    base_url = bu
    app.log.warn('Sending to server', url=base_url)
    buffer_dt = FLG.server_buffer_max_secs
    buffer_items = FLG.server_buffer_max_items
    data_in.pipe(
        op.buffer_with_time_or_count(buffer_dt, buffer_items),
        op.map(add_meta_data),
        remote_publish(token=FLG.token, hubs=base_url),
    ).subscribe(pass_, print)


def log_stats(rs):
    # addresses of clients in dt:
    dt = dict(stats['dt'])
    stats['dt'].clear()
    stats['dts'] = list(dt.keys())
    app.log.info('Stats', **stats)
    if FLG.per_sock_stats and dt:
        app.log.info('Per Socket Stats', **dt)
    return rs


data_flags = {'conf': {}}


def set_data_flags():
    def add(k, is_conf=False):
        if is_conf:
            data_flags['conf'][k[10:]] = getattr(FLG, k)
        else:
            data_flags[k[5:]] = getattr(FLG, k)

    [
        add(k)
        for k in dir(FLG)
        if k.startswith('data_') and not k.startswith('data_conf_')
    ]
    [add(k, True) for k in dir(FLG) if k.startswith('data_conf_')]


# ------------------------------------------------------------------------- App
def start():
    # to make the server use SSL, pass certfile and keyfile arguments to the
    # constructor
    h, p = host_port(FLG.bind)
    set_data_flags()
    handler = receive_msgpack if FLG.msg_fmt == 'msgpack' else receive_line_sep
    server = StreamServer((h, p), handler)
    if FLG.echo_socket:
        raise Exception('Not Yet Supported')
        app.log.info('Dispatching also to socket', dest=FLG.echo_socket)
        echo_sender_stream().subscribe(pass_, err_exit)
    url = FLG.server_url
    if not FLG.server_verify_ssl:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    cloud_sender_stream()  # .subscribe(pass_, err_exit)

    app.log.info('Opening ingress socket', host=h, port=p)
    try:
        server.serve_forever()
    except KeyboardInterrupt as ex:
        app.log.warn('KeyboardInterrupt')


if __name__ == '__main__':
    run_app(start)
# .
