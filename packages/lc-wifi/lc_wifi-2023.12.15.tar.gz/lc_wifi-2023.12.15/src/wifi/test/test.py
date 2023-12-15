import time
from operators.ops.tools import rx_operator
from importlib import import_module
from operators.con.sock import sock

socket_out = sock.snk


class test:
    socket_out = socket_out

    class load:
        """Producing load for tests"""

        class axtr:
            def make_reading(data_file='vf2', is_rx=True):
                m = import_module('wifi.data.assets.%s' % data_file)
                ctx = {}
                ctx['sample'] = m.sample

                def _make_reading(cpeid, msg):
                    data = dict(ctx['sample'])
                    data['ts'] = int(time.time() * 1000)
                    data['DeviceInfo']['SerialNumber'] = data['id'] = cpeid
                    return data

                return rx_operator(on_next=_make_reading)
