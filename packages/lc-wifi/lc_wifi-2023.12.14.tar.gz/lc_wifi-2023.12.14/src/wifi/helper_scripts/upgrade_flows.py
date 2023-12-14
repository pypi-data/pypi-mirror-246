#!/usr/bin/env python
"""
A tool which enables to convert flows w/o the con objects from 2022 to the new side effect connections
"""
import json
import os

from devapp.app import FLG, app, run_app
from devapp.tools import define_flags, exists, json_diff, read_file, write_file


def main():
    class Flags:
        autoshort = ''

        class flows_file:
            """existing flows file"""

            d = './flows.json'

        class action:
            n = 'Action to run'
            t = ['convert_from_ax_to_con_objects', 'none']
            d = 'none'  # TODO: allow empty string here

    run_app(run, flags=Flags)


def ident(o):
    return o


class Actions:
    def convert_from_ax_to_con_objects():
        fn = FLG.flows_file
        if not exists(fn):
            app.die('Not found', flows_file=fn)
        old_file = read_file(fn)
        old_flow = json.loads(old_file)
        flow = json.loads(old_file)
        app.info('Have flow', nodes=len(flow))
        rmops = []
        for op in flow:
            n = op.get('name')
            if not n:
                continue
            kw = op.get('kw', {})
            load, dump = ident, ident
            if isinstance(kw, str):
                load, dump = (json.loads, json.dumps)
            kw = load(kw)
            oldkw = dict(kw)
            def rm(*s, kw=kw):
                return [kw.pop(i, 0) for i in s]
            if 'redis' in kw:
                rm('redis')
            if n == 'buffer_by_tenant':
                id = op['id']
                ela = op['wires'][0][0]
                for op1 in flow:
                    for w in op1.get('wires', ()):
                        if id in w:
                            app.info('removing buffer_by_tenant', name=op1['name'])
                            w.remove(id)
                            w.append(ela)
                rmops.append(op)

            if n == 'configs_by_tenant':
                for v in kw.values():
                    e = v.get('elastic')
                    if e:
                        e.pop('hosts', 0)
            if (n + '.xx').split('.')[1] in (
                'redis',
                'kafka',
                'elastic',
                'http',
            ):
                assert n.split('.')[0] in ('ax', 'con')
                if n.startswith('ax.'):
                    op['name'] = 'con.' + n.split('.', 1)[1]
                    app.info('%s -> %s' % (n, op['name']), **op)
                if '.redis.' in n:
                    rm('port')
                elif '.kafka.' in n:
                    rm('config', 'enc', 'password')
                elif '.elastic.' in n:
                    rm('index')
                    rm('rotate')
                    rm('hosts')
                    rm('number_of_shards')
                    rm('http_auth')
            if kw != oldkw:
                op['kw'] = dump(kw)
        [flow.remove(o) for o in rmops]
        jd = diff(old_flow, flow, syntax='symmetric', marshal=True)
        if not jd:
            app.die('Nothing to change')
        app.info('changes', json=jd)
        fnb = '/tmp/flows.json.backup.%s' % os.getpid()
        write_file(fnb, old_file)
        write_file(fn, json.dumps(flow, indent=4))
        app.info('have written', file=fn, backup_old=fnb)


from jsondiff import diff

def run():
    return getattr(Actions, FLG.action, lambda x: 'no action')()

if __name__ == '__main__':
    main()
