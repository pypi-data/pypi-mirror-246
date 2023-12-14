import json
import os

import requests
from devapp.app import app
from devapp.tools import FLG, define_flags, offset_port


class Flags:
    class http_api_server:
        n = 'Node RED server host:port'
        d = '127.0.0.1:1880'


define_flags(Flags)


def headers(endpoint, verb='get'):
    verb = verb.lower()
    t = [endpoint, verb]
    headers = {'Content-Type': 'application/json', 'Node-RED-API-Version': 'v2'}
    if t == ['flows', 'post']:
        headers['Node-RED-Deployment-Type'] = 'full'
    return headers


def offs(hp):
    return '%s:%s' % (hp[0], offset_port(hp[1]))


G, P = requests.get, requests.post
get = lambda ep: G(BU() + ep, headers=headers(ep))
BU = lambda: 'http://%s/' % offs(FLG.http_api_server.split(':'))


def post(ep, data):
    data = json.dumps(data) if not isinstance(data, str) else data
    return P(BU() + ep, data=data, headers=headers(ep, verb='post'))


def get_flows():
    """Fetch flows from server"""
    r = get('flows').json()
    if r is None:
        app.info('Node RED has no flows')
    return r


def upload_flows(flow, nr_clear='full', ensure_hub=False):
    """Flow either list, json / string or filename"""
    if os.environ.get('skip_upload'):
        app.warn('Skipping upload of flow $skip_upload is set')
        return
    app.debug('Reconfiguring NodeRED. $skip_upload is NOT set.')
    if flow and nr_clear == 'full':
        # we spotted exceptions on NodeRed with sparsely assembled manual flows, w/o x and y using same ids
        # e.g. from test_mysql then test_proc: test_proc fails after test_mysql, since hi1 is considered rewired
        # Should be even faster, since Node-RED is not having to calculate merges.
        app.info('First clearing Node-RED')
        upload_flows([])
    if isinstance(flow, str) and os.path.exists(flow):
        with open(flow) as fd:
            flow = fd.read()
    flow = json.loads(flow) if isinstance(flow, str) else flow
    have = get_flows()
    if not have and flow == []:
        return
    if not nr_clear == 'full':
        flow = extend_flow(have['flows'], new=flow, mode=nr_clear)
    if ensure_hub and not any([op for op in flow if op['type'] == 'ax-hub']):
        tabs = [op for op in flow if op['type'] == 'tab']
        if not tabs:
            flow.insert(0, {'type': 'tab', 'id': 'test', 'name': 'Test'})
            tabs = flow
        hub = {'type': 'ax-hub', 'id': 'ax-hub', 'z': tabs[0]['id'], 'x': 200, 'y': 200}
        flow.insert(0, hub)
    r = post('flows', {'rev': have['rev'], 'flows': flow})
    if not r.status_code == 200:
        app.error('Status not 200', status_code=r.status_code, text=r.text)
        raise Exception('Status code != 200')
    r = r.json()
    r['flows'] = flow
    assert r['rev']
    return r


def extend_flow(old, new, mode):

    # replace all with same ids:
    nids = {op['id']: op for op in new}
    if mode.startswith('tab:'):
        # also repeat all of given tab:
        id = mode.split(':', 1)[1]
        nids.update({op['id']: op for op in old if op.get('z') == id or op['id'] == id})

    f = []
    for op in list(old):
        if op['id'] not in nids:
            f.append(op)
    f.extend(new)
    return f
