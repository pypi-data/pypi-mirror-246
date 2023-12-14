from devapp.app import app
from devapp.tools import now, partial as p
from gevent.server import StreamServer
import ujson as json

stats = {
    'data': 0,
    'err_decode': 0,
    'server_connects': 0,
    'err_server': 0,
    'batches': 0,
    'dt': {},
    'sockets': 0,
}


def receive_line_sep(socket, address, observer):
    # socket.sendall(b'Welcome to the echo server! Type quit to exit.\r\n')
    # using a makefile because we want to use readline()
    rfileobj = socket.makefile(mode='rb')
    addr = '%s:%s' % (address[0], address[1])
    stats['sockets'] += 1
    while True:
        line = rfileobj.readline()
        line = line.strip()
        if not line:
            break
        s = stats['dt'].get(addr)
        if not s:
            stats['dt'][addr] = s = [0, 0]

        try:
            v = json.loads(line)
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
        observer.on_next(v)
    rfileobj.close()


class Dispatcher:
    def readings(observer, host='0.0.0.0', port=16000):  # , data_conf=None):
        # data_conf = data_conf or None
        handler = p(receive_line_sep, observer=observer)
        server = StreamServer((host, port), handler)
        app.log.info('Opening ingress socket', host=host, port=port)
        try:
            server.serve_forever()
        except KeyboardInterrupt as ex:
            raise
