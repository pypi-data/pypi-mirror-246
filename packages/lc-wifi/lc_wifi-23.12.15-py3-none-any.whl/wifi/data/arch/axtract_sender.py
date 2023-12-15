#!/usr/bin/env python
from __future__ import print_function

import logging
import os
import sys
import ujson as json
import time
import socket


class AxWifiSender(object):
    def __init__(self, name, config, global_cfg):
        self.logger = logging.getLogger('%s.%s' % (__name__, name))
        self.host = config.get('host', '127.0.0.1')
        self.port = config.get('port', 1884)
        self.msg_fmt = config.get('msg_fmt', 'json')
        self.hostname, self.pid = socket.gethostname(), os.getpid()
        self.last_err_msg = 0
        self.log = self.logger.info
        self.config = config
        self.connect()
        self.logger.info('Module %s initialized' % name)

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            self.log('Connected to wifi socket server %s:%s' % (self.host, self.port))
            self.send({'sender': self.hostname, 'pid': self.pid})
        except Exception as ex:
            self.log_err(ex)

    def log_err(self, ex):
        """don't spam the log"""
        now = time.time()
        if self.last_err_msg > now - 5:
            return
        self.log(str(ex))
        self.last_err_msg = now

    def process_event(self, event):
        streamable_event = {'id': event.cpe.cpeid, 'ts': time.time()}
        streamable_event.update(event.props)

        self.logger.debug('Streamable event: %s' % streamable_event)
        res = self.send(streamable_event)
        self.logger.debug('Streamable result: %s' % res)

        return event

    def send(self, data):
        if self.msg_fmt == 'str':
            p = (str(data) + '\n').encode('utf-8')
        elif self.msg_fmt == 'json':
            p = (json.dumps(data) + '\n').encode('utf-8')
        try:
            self.socket.sendall(p)
            return 'sent %s bytes' % len(data)
        except Exception as ex:
            self.log_err(ex)
            self.connect()

    def close(self):
        pass


if __name__ == '__main__':
    s = AxWifiSender('test_sender', {}, {})

    class ev:
        props = {'a': 'b'}

        class cpe:
            cpeid = 'testcpe'

    print(s.process_event(ev))
