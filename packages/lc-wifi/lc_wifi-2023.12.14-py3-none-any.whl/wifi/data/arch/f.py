#!/usr/bin/env python
import os, sys, time, uuid
from node_red import nrclient as red, log
from devapp.app import run_app, app
from functools import partial as p

from random import randint


class Functions:
    class foo:
        def filipe(data):
            breakpoint()  # FIXME BREAKPOINT
            return data


def start():
    red.connect(Functions)


if __name__ == '__main__':
    run_app(start)

# -------------------------------------------------------------
# import unittest
# from node_red import nrtesting as nrt


# class SumMult(unittest.TestCase):
#     flow = nrt.flow_linear(
#         [
#             'math:sum',
#             'math:modulo',
#             {'type': 'ax-map', 'name': 'math:mult', 'kw': {'weight': 10}},
#             'math:div',
#         ]
#     )

#     def setUpClass():
#         T = SumMult
#         T.nr = nrt.configure_node_red(T.flow)
#         nrt.do_connect(Functions)

#     def setUp(self):
#         nrt.log_store.clear()

#     def test_simple(self):
#         res = nrt.get_job_res({'a': 2, 'b': 3}, self.nr)
#         assert (
#             res['modulo'] == res['b'] % res['a']
#             and res['sum'] == 5
#             and res['mult'] == 60
#             and res['div'] == res['a']
#         )

#     def test_simple_again(self):
#         """mainly a reconnect test"""
#         return self.test_simple()

#     def test_map_func_err(self):
#         """Causing an exception in a stream function, want all the infos"""
#         self.nr.send({'payload': {'a': 0, 'b': 3}})
#         errs = nrt.wait_for_log_ev('ZeroDivision', wait=1)
#         assert len(errs) == 1
#         e = str(errs)
#         # we want original err, traceback and causing message and operator in the error:
#         assert 'ZeroDivision' in e  # original error reason
#         assert "data['modulo'" in e  # traceback
#         assert "'a': 0" in e  # causing msg
#         assert 'wires' in e  # operator
#         print('Got expected ZeroDivision error out of band.')
#         # stream must be catched:
#         res = nrt.get_job_res({'a': 2, 'b': 3}, self.nr)
#         for k, v in {
#             'a': 2,
#             'b': 3,
#             'div': 2.0,
#             'modulo': 1,
#             'mult': 60,
#             'sum': 5,
#         }.items():
#             assert res[k] == v


# class StreamSplitting(unittest.TestCase):
#     flow = nrt.flow_linear(
#         [
#             'math:sum',
#             {
#                 'type': 'ax-cond',
#                 'name': '',
#                 'condition': '[["payload.sum", "<", 10], true]',
#             },
#             [
#                 [
#                     'math:mult',
#                     {
#                         'type': 'ax-map',
#                         'name': 'math:mult',
#                         'kw': {'d1': 'mult', 'd2': 'sum', 'weight': 10},
#                     },
#                 ],
#                 ['math:sum'],
#             ],
#         ]
#     )

#     @classmethod
#     def setUpClass(T):
#         T.nr = nrt.configure_node_red(T.flow)
#         nrt.do_connect(Functions)

#     def test_first_substream_when_cond_matches(self):
#         res = nrt.get_job_res({'a': 2, 'b': 3}, self.nr)
#         assert res['mult'] == 300  # 5 * 6 * 10 (sum * mult * weight, upper path)

#     def test_second_substream_when_catchall_cond_matches(self):
#         res = nrt.get_job_res({'a': 5, 'b': 5}, self.nr)
#         assert res.get('mult') == None
#         assert res.get('sum') == 10


# def payload(test, **kw):
#     kw['test'] = test
#     return {'payload': kw}


# class AsyncSplitting(unittest.TestCase):
#     flow = nrt.flow_linear(
#         [
#             'math:sum',
#             {
#                 'type': 'ax-cond',
#                 'name': '',
#                 'condition': '[["payload.sum", "<", 10], true]',
#             },
#             [
#                 [
#                     {'type': 'ax-map', 'name': 'time:sleep', 'async_timeout': 0.05,},
#                     'math:sum',
#                 ],
#                 ['math:mult', 'math:sum', 'math:div', 'math:modulo',],
#             ],
#         ]
#     )

#     @classmethod
#     def setUpClass(T):
#         T.nr = nrt.configure_node_red(T.flow)
#         nrt.do_connect(Functions)

#     def setUp(self):
#         nrt.log_store.clear()

#     def test_async(self):
#         c = []
#         d = red.subj_snd.subscribe(lambda msg: c.append(msg))
#         # self.nr.send({'payload': {'a': 2, 'b': 1}})
#         # elf.nr.send({'payload': {'a': 9, 'b': 2}})
#         # red.gevent.spawn(self.nr.send, {'payload': {'a': 2, 'b': 1}})
#         # red.gevent.spawn(self.nr.send, {'payload': {'a': 9, 'b': 2}})
#         pl = p(payload, 'test_async')

#         self.nr.send(pl(a=2, b=1, sleep=0.01))
#         self.nr.send(pl(a=9, b=2))
#         while not len(c) == 2:
#             time.sleep(0.001)
#         d.dispose()
#         assert [m['payload']['b'] for m in c] == [2, 1]

#     def test_async_timeout(self):
#         """the sleep of the first substream will timeout
#         Lets assert that
#         """
#         c = []
#         d = red.subj_snd.subscribe(lambda msg: c.append(msg))
#         uid = str(uuid.uuid4())
#         self.nr.send(payload('asyn_timeout', a=2, b=3, sleep=0.06, id=uid))
#         err = nrt.wait_for_log_ev('TimeoutError')[-1]
#         print('Got expected timeout error out of band.')
#         assert uid in str(err)
#         assert not c  # no result was sent
#         res = nrt.get_job_res({'a': 15, 'b': 3}, self.nr)
#         assert res['modulo'] == 3


# class TestPerf(StreamSplitting):
#     # only standalone
#     def xtest_perf_indication(self):
#         nrt.log_drop_evs.append(1)
#         t0 = time.time()
#         for i in range(1000):
#             self.nr.send({'payload': {'a': 2, 'b': 3}})
#         print('Time for 1000 events', time.time() - t0)
#         nrt.log_drop_evs.clear()
