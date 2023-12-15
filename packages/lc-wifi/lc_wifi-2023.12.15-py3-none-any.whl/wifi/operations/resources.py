# currently no specific resources - only constants for the project.
from os.path import dirname
from devapp.tools.resource import add_const, exists, write_file
from devapp.tools import project
from devapp.app import app
from os import environ as env
import os
from node_red.operations.resources import worker as lcpy_worker, rsc as lcpy_rsc
from functools import partial
from shutil import copyfile


# for npm installer / project creation:
n = dirname
d = n(n(__file__))
f = d + '/js/nodered/flows_lib/default_flows.json'
add_const('fn_flows', f)
add_const('hub_title', 'AXWIFI 2.6')
add_const('client_import', 'from wifi import WiFiFunctions')
add_const('client_base', 'WiFiFunctions')


def client(*a, **kw):
    kw['tab'] = 'AXTRACT,AXWIFI'
    return do(*a, **kw)


def usp(*a, **kw):
    kw['tab'] = 'AXUSP,AXWIFI'
    return do(*a, **kw)


def api(*a, **kw):
    kw['tab'] = 'API,AXWIFI'
    return do(*a, **kw)


def do(*a, **kw):
    ensure_inject_nodes_data_files_present()
    return lcpy_worker.cmd_(*a, **kw)


def ensure_inject_nodes_data_files_present():
    d = project.root() + '/data/inject'
    if exists(d):
        return
    os.makedirs(d)
    ds = n(__file__) + '/inject'
    [copyfile(ds + '/' + k, d + '/' + k) for k in os.listdir(ds) if k.endswith('.json')]
    app.info("copied inject nodes data files over", dest=d)


class rsc:
    class client(lcpy_rsc.client):
        n = 'AXWiFi Worker Process.'
        cmd = client

    class api(lcpy_rsc.api):
        n = 'AXWiFi API.'
        cmd = api

    class usp(lcpy_rsc.worker):
        n = 'AXWiFi USP'
        cmd = usp
        systemd = 'usp'
