"""
Edit [2022-03-27 09:47] : This one should go out of service - was heavily in use for the first mocha based
tests, later migrated to test_misc_node_red.py.
-------------------------------------------------------------------------------------------

Tools for testing the client

Design: The client is normally started (run_app) with owned logging nd and stream mgmt.

=> The client runs IN PROCESS of the test!

=> Thats why the test program stays OUTSIDE of the app, has own logging, does NOT use / interfere rx streams but use lalaland polling and events on the time axis.

Node red is started by mocha, restarted (at a new port) at every flow reconfig from the test client - sent via the normal websockt into NR.


Test ingress and reconfigure traffic is sent from this test client to mocha via the normal
ws ingress, not the hub ws. Default endpint: /ws/tests/default


ADDENDUM 2020: Far easier test setups via actual node red running, using its http api to upload flows. See e.g. test_subflows
"""

import json
import os
import subprocess as sp
import sys
import time
import unittest
from functools import partial
from threading import Event, current_thread

import gevent
import websocket  # noqa
from devapp.app import app, run_app
from gevent import monkey
from node_red.draw import graph_easy  # noqa
from node_red.nr_config_builder import (
    ax_op,
    cond,
    escaped_flow,
    nr_config,
    op,
    rx_op,
)  # noqa
from node_red.nrclient import connect, js, subj_snd, subj_sts
from node_red.testing import AsyncClient, Event  # noqa
from operators.core import ax_core_ops
from structlogging.sl import DropEvent, std_processors  # noqa

monkey.patch_all()


now = time.time
port_ax_hub = 1882  # FIXME this will be dynamic
# same container setup for now:
d_inst_NR = '/root/.node-red'
fn_srv_js = 'server_for_python_tests'
fn_test_server = d_inst_NR + '/ax/test/py/' + fn_srv_js
nr_start_mode = 'detect'  # start|detect|<port>

# -------------------------------------------------------------- Base Class For Testing
wait = lambda dt: time.sleep(dt)
ax = ax_core_ops


def setup_NRT(f, T):
    """
    allows to have specific flows for tests in NRT classes
    typically run in setUpClass of NRT
    """
    T.flow = nr_config(
        f, wrap_dflt_all=T.wrap_dflt_all, add_nr_io=True, funcs_namespace=T.Functions
    )
    exit_on_env_printflow_set(T.flow)
    # T.graph = draw(T.flow)
    T.nr = configure_node_red(T.flow)
    # print(yaml.dump(T.flow))  # testoutput better in yaml for complex ones
    do_connect(T.Functions)


class NRT(unittest.TestCase):
    """Adding some convenience Functions for Tests with Node Red Process"""

    f = None  # the "convenience flow", manually writting in tests, not yet final NR format
    flow = None  # final json format for NR
    wrap_dflt_all = True
    Functions = None  # when using this, set it to your test functions
    graph = None

    @classmethod
    def setUpClass(T):
        print()
        print(title(T.__name__))
        # allows to conveniently run setup_NRT in the tests of an NRT class
        T.setup = partial(setup_NRT, T=T)

        if T.f:
            T.setup(T.f)

    def setUp(self):
        log_store.clear()
        # Clear the core snk (this has no event)
        s = ax.snk
        l = self.ax_mem_snk = s._mem_snk
        e = self.ax_mem_snk_ev = s._mem_snk_last_event
        l.clear()
        e.clear()
        e.append(Event())
        # test_func_doc(graph=self.graph)

    def get_mem_snk_content(self, expect=None):
        """helper"""
        l = self.ax_mem_snk
        if expect != None:
            t0 = now()
            while len(l) < expect and now() - t0 < 1:
                wait(0.01)
            return l

        self.ax_mem_snk_ev[0].wait(5)
        assert self.ax_mem_snk_ev[0].is_set()
        return l

    def ws_client(self, **kw):
        """helper for websock tests"""
        oe, ce, w = Event(), Event(), self.nr
        ws = TestWebsock(oe, ce, host=w.host, port=w.port, **kw)
        gevent.spawn(ws.run_forever)
        oe.wait(10)
        return ws


# ------------------------------------------------------------------------- NRT Helpers


def payload(test, **kw):
    """helper for raw ws.send, i.e. w/o blocking for result"""
    kw['test'] = test
    return {'payload': kw}


n_mem_snk = op.ax.snk_mem


# -------------------- logging - we stay outside the app, don't use it's logging system


class ta:
    # testapp: we do our own "logging", to not interfere with the app's structlogging:
    now = lambda: int(time.time() * 1000)
    t0 = now()
    dt = lambda: ta.now() - ta.t0

    def tt():
        cn = current_thread().name.replace('Dummy', '')
        return '%7s | %12s | ' % (ta.dt(), cn)

    def out(msg, **kw):
        print(ta.tt(), msg.upper(), kw if kw else '')

    def die(msg, **kw):
        msg += 'ERR! '
        ta.warn(msg, **kw)
        sys.exit(1)

    info = warn = debug = out


# ------------------------------------------------------- Tapping the produced logs
log_store = []
log_drop_evs = []


def wait_for_log_ev(match, wait=4):
    t0 = time.time()
    while time.time() - t0 < wait:
        l = [ev for ev in log_store if match in str(ev)]
        if l:
            return l
        time.sleep(wait / float(10))
    raise Exception('timeout waiting for %s' % match)


def add_log_to_store(_, level, ev, ls=log_store):
    if log_drop_evs:
        raise DropEvent
    ls.append(dict(ev))
    return ev


# ------------------------------------------------------------- Starting the client
def do_connect(Funcs):
    """announcing us as the client, with our funcs to test"""
    # breakpoint()  # FIXME BREAKPOINT
    con = lambda hubs='127.0.0.1:%s' % state['ws'].port: connect(Funcs, hubs)
    if not state['app']:
        std_processors().append(add_log_to_store)
        con = lambda con=con: run_app(con)
        state['app'] = app
    gevent.spawn(con)

    wait_for = lambda msg: (
        msg and msg['type'] == 'status' and msg['payload'] == 'registered'
    )
    res = AsyncClient.wait_blocking_for_client(subj_sts, wait_for)
    return res


def get_job_res(job, nr, msgs=1, payload_only=True):
    nr.send({'payload': job})
    res = AsyncClient.wait_blocking_for_client(
        subj_snd, lambda msg: msg['type'] == 'msg', msgs=msgs
    )
    ta.info('got job result(s)', res=res)
    return res['payload'] if (msgs == 1 and payload_only) else res


# ---------------------------------------------------- end blockin test script wrappers
# some tests use a file writer to here:
# FIXME eliminiate this, old :
fn_test_msgs = os.environ['HOME'] + '/tmp/test_msgs'


def unlink_test_msgs():
    if os.path.exists(fn_test_msgs):
        os.unlink(fn_test_msgs)


def read_test_msgs_file(wait=1, wait_for=None):
    s = ''
    t0 = now()
    while now() < (t0 + wait):
        time.sleep(0.05 if wait_for else wait)
        with open(fn_test_msgs) as fd:
            s = fd.read()
        if wait_for and wait_for in s:
            break

    def try_parse(l):
        try:
            return json.loads(l)
        except Exception:
            return l

    l = [try_parse(sl) for sl in s.splitlines()]
    return l


class TestWebsock(websocket.WebSocketApp):
    """
    We have no http endpoint to control our NR test server, so we send our tests over via this one.
    This is, naturally, not the websock for the biz traffic, just test control (we send new flow configs, triggering restarts of NR on the other side)

    """

    def __init__(
        self, openev, closeev, host=None, port=None, path=None, tab='tests', flow='dflt'
    ):
        """path, when set, overrules tab/flow as pth"""
        self.openev, self.closeev = openev, closeev
        if not port:
            host, port = get_node_red(ts=nr_start_mode)
            self.port = port
            self.host = host
        if not path:
            path = '/ws/%s/%s' % (tab, flow)
        self.url = 'ws://%s:%s%s' % (host, port, path)
        ta.info('opening ws', url=self.url)
        super().__init__(
            self.url,
            on_close=self.on_close,
            on_message=self.on_message,
            on_open=self.on_open,
        )
        ta.info('created ws', url=self.url)
        self.messages = []

    def on_message(self, msg):
        """
        This client is normally only used to send reconfigs to mocha
        -> we do not expect messages from the server - except for tests, so we log them:
        """
        print('test client got msg', msg)
        self.messages.append(msg)

    def on_open(self):
        ta.info('test socket opened')
        self.openev.set()

    def on_close(self):
        ta.info('test socket closed')
        self.closeev.set()

    def send(self, msg):
        super().send(js(msg))


state = {'ws': None, 'app': None}


def title(s):
    print()
    print('=' * len(s))
    print(s)
    print('=' * len(s))


def open_ws():
    oe, ce = Event(), Event()  # open event, close event
    state['ws'] = w = TestWebsock(oe, ce)
    gevent.spawn(w.run_forever)
    oe.wait(10)
    if not oe.is_set():
        ta.die('comm problem with test server', phase='init')
    state['close_ev'] = ce


# just so that nrt holders can access that:
cur_test_flow = [0]
cur_nr = [0]


def configure_node_red(flow):
    """
    For convenient setUpClass methods in tests:
        self.nr = nrt.configure_node_red(self.flow)

    Gets host port of running node red, or starts it at first run.
    Then injects test flow (leading to ws close), reconnects
    """
    # after startup we send the flow, which disables our connection, i.e. we reconnect:
    if not state.get('ws'):
        # Startup, lets get an initial connection:
        # remove any pytest cli args, would break FLGs:
        set_sys_argv()
    first = True
    while True:
        try:
            if first:
                open_ws()
                first = False
                time.sleep(0.1)
            ta.info('Sending Test Flow - socket will close')
            state['ws'].send({'reconfigure': flow})
            cur_test_flow[0] = flow
            state['close_ev'].wait(10)  # close event, after flow
            open_ws()
            nr = cur_nr[0] = state['ws']
            return nr
        except Exception as ex:
            breakpoint()  # FIXME BREAKPOINT
            open_ws()


def find_test_NR_host_port(pid):
    """derive running port of test server"""
    while True:
        cmd = 'netstat -tanp | grep %s/server | grep -v %s'
        cmd = cmd % (pid, port_ax_hub)

        l = os.popen(cmd).read()
        if not l.strip():
            ta.debug('No listen addr yet')
            time.sleep(0.4)
            continue
        h, p = l.split()[3].split(':')
        ta.info('testserver listen addr', host=h, port=p)
        return h, int(p)


def set_sys_argv():
    # remove any pytest cli args, would break FLGs:
    # coverage:pytest.py, else pytest. and yes, its shit.
    # TODO: create a conf + fixture, avoiding this:

    if 'pytest' not in sys.argv[0].rsplit('/', 1)[-1]:
        return
    while len(sys.argv) > 1:
        sys.argv.pop()

    e = os.environ
    dflts = {
        'environ_flags': True,
        'log_level': 10,
        'log_time_fmt': 'dt',
        'log_add_thread_name': True,
        'log_dev_fmt_coljson': 'pipes,cfg,payload',
    }
    for k, v in dflts.items():
        v = e.get(k, v)
        print('pytest EnvFlag: %s->%s' % (k, v))
        if v:
            e[k] = str(v)


def detect_hub_in_process_list(start_js):
    """this actually belongs better into nrtesting but maybe it establishes itself
    (if provisioning is too tedious and we always in pods - why not)
    """
    if os.environ.get('CONTAINER_NAME') and os.environ.get('container'):
        pid = '-'
        cmd = 'netstat -tanp |grep -v 188 | grep LISTEN | grep 0.0.0.0 '
        cmd += "| grep node | cut -d ':' -f 2 | cut -d ' ' -f 1"
        t0 = time.time()
        while time.time() < t0 + 10:
            p = os.popen(cmd).read()
            try:
                return '127.0.0.1', int(p.strip())
            except Exception as ex:
                time.sleep(0.1)
        raise TimeoutError('Waiting for server', p)
    i = -1
    while i < 5:
        i += 1
        # might be startd with --inspect, i.e. 2 processes, we need the node one then
        # otherwise we need the mocha one:
        cmd = 'ps wwwax | grep " %s" | grep -v grep | head -n 2 ' % start_js
        pid = os.popen(cmd).read().strip().splitlines()
        ta.info('Finding local test hub (dynamic port) in ps list', cmd=cmd, pid=pid)
        if pid:
            # when he was running at our start we have it
            if i == 0:
                break
            # otherwise it might be started with --inspect, i.e. WILL start node as fork,
            # we need node - so lets wait another cycle:
            i = -1
        time.sleep(2)
    if not pid:
        ta.die('no testserver pid found', process=fn_srv_js)
    filt = '/bin/mocha '
    if len(pid) == 1:
        filt = 'xx'
    pid = [l for l in pid if filt not in l][0].strip().split(' ')[0]
    ta.info('testserver found up', pid=pid)
    h, p = find_test_NR_host_port(pid)
    print('Host, port', h, p)
    return h, p


def get_node_red(ts):
    """ts may be given fixed port where a server is already up
    or 'detect', then we find out the port
    or 'start', then we start one as subproc
    
    """
    if ts.isdigit():
        host, port = '127.0.0.1', int(ts)
    elif ts == 'detect':
        # mocha is NR's default test runner. when run in inspect mode its starting NR as subproce, so exclude it from finding actual pid:
        host, port = detect_hub_in_process_list(fn_srv_js)
    elif ts == 'start':
        host, port = start_test_server()
    else:
        raise
    return host, port


def start_test_server():
    w = '10000000000000'  # without inspect, tests would timeout
    node = sp.Popen(['mocha', '-t', w, fn_test_server], cwd=d_inst_NR + '/ax')
    host, port = find_test_NR_host_port(node.pid)
    return host, port
