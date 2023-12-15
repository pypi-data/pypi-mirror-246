#!/usr/bin/env python
from __future__ import print_function
import gevent
from gevent import monkey

monkey.patch_all()
import json
import time

# -*- coding: utf-8 -*-

import confluent_kafka
import pickle
import time


def get_producer(config):
    cfg = {
        'bootstrap.servers': config['bootstrap_servers'],
        # Wait 100ms for other events, so we send a nice batch.
        'queue.buffering.max.ms': 100,
        'log.connection.close': False,
        'api.version.request': True,
        'error_cb': error_cb,
    }

    cfg.update(config['options'])

    producer = confluent_kafka.Producer(dict(cfg))
    return producer


def on_delivery_cb(self, msg):
    print('Error: %s' % msg.error())
    print('Value: %s' % msg.value())


def error_cb(err):
    print('Kafka error: %s: %s', err.name(), err.str())


def event_to_kafka(cpeid, config, event):
    producer = get_producer(config)

    topic = config['topic']
    block = config['block']

    # pickled_event = pickle.dumps(event, pickle.HIGHEST_PROTOCOL)

    while True:
        # try:

        tevent['ts'] = int(time.time() * 1000)
        pickled_event = pickle.dumps(event, 2)
        producer.produce(
            topic=topic, value=pickled_event, key=cpeid, on_delivery=on_delivery_cb,
        )
        # except BufferError:
        #    if block:
        #        producer.poll(timeout=0.5)
        #        continue
        #    return {"code": 501, "msg": "Kafka error: Buffer full."}

        # try:
        producer.poll(timeout=0)
        # except Exception as error:
        #    pass
        time.sleep(1)

    return producer, {'code': 200, 'msg': 'Successfully pushed the event to Kafka.'}


if __name__ == '__main__':
    tcpeid = '603197-S172V24000016'

    tconfig = {
        'topic': 'wifi_results',
        'block': False,
        'bootstrap_servers': '192.168.29.104:9092',
        #'bootstrap_servers': '192.168.29.104:9092',
        'options': {
            'security.protocol': 'sasl_plaintext',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': 'axtract',
            'sasl.password': 'J1UTBLQE9VB89JD3',
        },
    }

    with open('d2') as fd:
        tevent = fd.read()
        tevent = eval(tevent)

        tevent['job'] = {
            'steps': {
                '1': {
                    'MappedSetParameterValues': {
                        'WiFi.Radio.2.Channel': 1,
                        'WiFi.Radio.2.AutoChannelEnable': 0,
                        'WiFi.Radio.5.Channel': 102,
                        'WiFi.Radio.5.AutoChannelEnable': 0,
                    }
                }
            }
        }

    # tevent = {'test': 'test'}
    prd, res = event_to_kafka(tcpeid, tconfig, tevent)

    # Only here in this test-script it is needed to wait for the sending.
    # get_producer(tconfig).flush(2)
    prd.flush(1)
    print(res)
    # time.sleep(0.01)
