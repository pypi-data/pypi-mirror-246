from devapp import gevent_patched  # noqa
import json
import os
import time
from functools import partial
import json

# --------------------------------------------------------------------------- utilities
from socket import socket
from threading import Event as Event_

import gevent
import websocket
from devapp.app import FLG, app, run_app
from devapp.tools import Pytest, write_file, offset_port
from gevent.event import Event
from node_red import http_api as api
from node_red import nrclient as red
from operators.core import AX, ax_core_ops
from rx import operators as rx

pth = os.path


def tlog(msg, **kw):
    kw = ', '.join(['%s: %s' % (k, v) for k, v in kw.items()])
    with open('/tmp/testlog', 'a') as fd:
        fd.write('%s %s\n' % (msg, kw))


class TestFlow:
    now = time.time

    def locate(nofail=False):
        """
        Finding the fullpath of the testflow for a test, assuming that:

        1.) When d be <test mod filename w/o test_ and .py>
        2.) Then flow is found in subdirectory flows/<d>/<fn_flow_json>.json

        Example:
        _ = '/opt/repos/lc/python/node_red/tests' # example dir
        fn_test_mod = _ + '/test_http_simple.py'
        fn_flow_json = 'single_func'

        This is then loaded:
        _ + '/flows/http_simple/single_func.json'

        We derive the infos from $PYTEST_CURRENT_TEST
        """
        m = Pytest.parse_test_infos()
        print('-' * 80)
        print(m['test'])
        fn_test_mod = m['path']
        d = fn_test_mod.rsplit('/', 1)[-1]
        # if d.startswith('test_'):
        #    d = d[5:]
        if d.endswith('.py'):
            d = d[:-3]
        d = pth.dirname(pth.abspath(m['path'])) + '/flows/%s' % d
        fn_flow = d + '/%s.json' % m['test']
        if not pth.exists(fn_flow) and not nofail:
            app.die('Test Flow not found: %s' % fn_flow, **m)
        return fn_flow

    def create():
        """Tool to create a test flow from the current active node red flow
        Intended to be used once per test, for getting the flow, e.g.:

        def test_2_py_op_debug_out()
            return TestFlow.create()

        Will download the current node red flow, reindex it, then put it into the
        correct location. After that you can write your stimuli and result assertions.
        Correction location is flows/<modulename>/test_2_py_op_debug_out.json in the
        example
        """
        fn = TestFlow.locate(nofail=True)
        from node_red import http_api as api

        f1 = api.get_flows()
        from operators.bin.flow_file_tools import Actions

        f = Actions.reindex(f1['flows'], as_json=True)
        write_file(fn, f, log=2, mkdir=1)
        m = 'Created' if not os.path.exists(fn) else 'Overwritten'
        app.info(m + ' test file', fn=fn, info='Ready to run tests.')

    def get_op(flow, key, value):
        r = [op for op in flow if op[key] == value]
        if len(r) != 1:
            app.die('Found ops', key=key, value=value, ops=r)
        return r[0]

    def add_wire(flow, frm=None, **crit):
        """add_wire(f, frm=<id>, to=<id2>)"""
        to = crit.pop('to')
        if frm:
            crit['id'] = frm
        for n, v in crit.items():
            op = TestFlow.get_op(flow, n, v)
            op['wires'][0].append(to)


# --------------------------------------------------------------------- Connect Client
class Event(Event):
    pass


class Client:
    def connect(Functions=AX):
        run_app(partial(red.connect, Functions))


class AsyncClient:
    # at testing we want high timeouts, for brkpoint inspectsion, normally 1 sec enough:
    def wait_blocking_for_client(subj, wait_for, timeout=10, msgs=1):
        """
        Helper to block for client in stream results.

        state changes of the client are normally made known to the hub - e.g. are available on status update subject (subj_sts).
        So we tap here to learn about the state of the client under test.
        """
        ev = Event()
        res = []
        d = []

        def set(msg, ev=ev, msgs=msgs, res=res):
            res.append(msg)
            # print('got', len(res), msgs, wait_for, subj)
            if len(res) == msgs:
                d[0].dispose()
                ev.set()

        d.append(subj.pipe(rx.filter(wait_for)).subscribe(set))
        ev.wait(timeout)
        if ev.is_set():
            if msgs > 1:
                return res
            # this is needed, e.g. at register call back from client: hub needs a little time to register the new functions and we don't want to poll the hub here:
            # TODO: invent a verify ping/pong event from the client
            wait(0.01)
            ##tlog(str(res))
            return res[0]
        print('Got msgs until timeout:')

        print(json.dumps(res, indent=2, default=str))
        raise TimeoutError('Timed out waiting for event')

    def wait_for_status(payload='registered', timeout=10):
        def wait_for(msg, pl=payload):
            if msg and msg['type'] == 'status' and msg['payload'] == pl:
                return True

        wait = AsyncClient.wait_blocking_for_client
        return wait(red.subj_sts, wait_for, timeout=timeout)

    def connect(Functions=AX, hub_recon_intv=0.1, timeout=10):
        """announcing us as the client, with our funcs to test"""

        Pytest.set_sys_argv()

        greenlet = gevent.spawn(
            run_app,
            partial(red.connect, Functions, hub_recon_intv=hub_recon_intv),
            call_main_when_already_running=True,
        )
        greenlets.append(greenlet)
        res = AsyncClient.wait_for_status(timeout=timeout)
        return res


now, wait = time.time, time.sleep
greenlets = []
# ------------------------------------------------------- blocking test script wrappers
class Event(Event_):
    """Allows to add attrs, gevent's does not"""


def wait_for_obj(obj, count=None, until=1, then=None, hold=0):
    """Block polling, until obj is truthy"""
    t0 = now()
    while now() - t0 < until:
        if obj and (count is None or len(obj) >= count):
            wait(hold)  # a little time to wait for more msgs
            if then:
                then()
            return obj
        wait(until / 20.0)
    raise TimeoutError('waited %ss' % until)


from operators.con import connections, sock


def sock_send_rcv(flow):
    client = AsyncClient
    add = connections.add_connection

    add(sock.sock, 'test_comm_sock', port=1887)

    f = api.upload_flows(flow)['flows']
    c = client.connect()
    with socket() as socks:
        socks.connect(('127.0.0.1', offset_port(1887)))
        t0 = now()
        res = socks.send(b'foo\n')
        res = socks.recv(1024)
        res = res.decode('utf-8')
        res = json.loads(res)
        to = FLG.op_join_default_timeout
        # immediate join, based on message count, not timeout
        assert now() - t0 < to / 2.0
        return res


# -------------------------------------------- Websocket client


class WebSocket(websocket.WebSocketApp):
    def __init__(self, pth, on_msg, host='127.0.0.1', port=1880):
        port = offset_port(port)
        self.url = 'ws://%s:%s%s' % (host, port, pth)
        super().__init__(self.url, on_message=on_msg, on_open=self.on_open)

    def on_open(self):
        app.info('Opened websocket', url=self.url)


def open_websocket(pth, **wait_for_obj_kw):
    """convenience func returning not only open ws but also msgss container"""

    msgs = []

    def add(self, pl, into=msgs):
        into.append(json.loads(pl))

    ws = WebSocket('/ws/out2', add)
    gevent.spawn(ws.run_forever)
    kw = wait_for_obj_kw
    if kw:
        kw['then'] = ws.close if kw['then'] == 'ws.close' else kw.get('then')
        wait_for_obj(msgs, **kw)
    return ws, msgs


def insert_test_graph_into_test_module(flow):
    '''
    More archive than antyhing else:
    Total hack to add the boxart into a pytest module (mocha)
    We keep it but its a stupid hack, replaceing ** in all docstrings with """**...
    with the graph.
    Should be used right at build.py def build_flows
    TODO: clean up, use a fckng regex
    '''
    from node_red.draw.graph_easy import draw

    f = draw(flow, id_short_chars=12, no_print=True)
    fn = '/tmp/f.py'
    with open(fn) as fd:
        s = fd.read()
    import os

    pt = os.environ['PYTEST_CURRENT_TEST'].split('::')
    cpre, cpost = s.split('\nclass %s' % pt[1], 1)
    tn = pt[2].split(' ', 1)[0]
    pre, post = cpost.split('\n    def %s' % tn, 1)
    A = post.split('\n', 2)
    sep = '"""**'
    if sep in A[1]:
        f = f.replace('\n', '\n        ').replace('** Tab Tests', '')
        gr = '"""\n        ' + f + '\n'
        s = (
            cpre
            + '\nclass %s' % pt[1]
            + pre
            + '\n    def %s' % tn
            + A[0]
            + '\n'
            + A[1].replace(sep, gr)
            + '\n'
            + '        '
            + A[2].lstrip()
        )
    with open(fn, 'w') as fd:
        fd.write(s)
