#!/usr/bin/env python
import websocket
import gevent
from gevent import monkey
from functools import partial as p
import ujson
import rx as Rx
import sys
import re
import time
import traceback
from rx import subject, operators as rx
from rx import scheduler
from rx.scheduler.eventloop import GEventScheduler
from operator import setitem
from log import info, warn

run = Rx.Observable.run
monkey.patch_all()

GS = GEventScheduler(gevent)

hubs = {}
flows = {}  # configured known node red flows

s_all_msgs = Rx.subject.subject.Subject()

js = lambda struct: ujson.dumps(struct, ensure_ascii=False)
jp = lambda s1: ujson.loads(s1)


def noop(r):
    breakpoint()  # FIXME BREAKPOINT


class MsgHandlers:
    def on_register(msg):
        ws = hubs[msg['hp']]['ws']
        ws.sid = msg['sid']
        m = {'type': 'registration', 'funcs': Funcs}
        print('sending')
        send(ws, m)
        print('complete')
        return msg

    def on_job(msg):
        print('job')
        ws = hubs[msg['hp']]['ws']
        msg['type'] = 'jobres'
        fn = msg['func']
        func = Funcs.get(fn)

        if not func:
            msg['err'] = 'function not found'
        else:
            try:
                msg['res'] = func(msg['payload'])
            except Exception as ex:
                exc_type, exc_value, exc_tb = sys.exc_info()
                tb = traceback.format_exception(exc_type, exc_value, exc_tb)
                msg['err'] = str(ex)
                msg['err_details'] = {'tb': tb}
        send(ws, msg)
        return msg


def func_by_type(s):
    typ = s.key
    func = getattr(MsgHandlers, 'on_' + typ, noop)
    print('func', func)
    return s.pipe(rx.map(func))


def dbg(r):
    print('have', r)
    return r


s_msgs_processed = s_all_msgs.pipe(
    rx.map(dbg), rx.group_by(lambda msg: msg['type']), rx.flat_map(func_by_type),
)


class WebSocket(websocket.WebSocketApp):
    sid = None  # at register

    def __init__(self, host, port, obs):
        self.hp = hp = (host, port)
        self.obs = obs
        url = 'ws://%s:%s/ws/hub' % self.hp
        hubs[tuple(hp)] = {'status': 'init', 'ws': self}
        self.info = p(info, hub=self.hp)
        self.cid = 'host1.py1'  # client id. should be telling. from config. somehow
        super().__init__(
            url,
            on_message=self.on_message,
            on_close=self.on_close,
            on_open=self.on_open,
        )

    def on_open(self):
        self.info('open')
        return

    def on_close(self):
        self.info('close')

    def on_message(self, msg):
        hp = self.hp
        msg = jp(msg)
        msg['hp'] = hp
        self.info('msg', **msg)
        hubs[hp]['status'] = 'alive'
        typ = msg['type'] = msg['type']
        s_all_msgs.on_next(msg)


def produce(obs, scheduler, h, p):
    while True:
        ws = WebSocket(h, p, obs)
        ws.run_forever()
        time.sleep(1)


def main(_cid):
    global cid
    cid = _cid
    # websocket.enableTrace(True)
    s_msgs_processed.pipe(rx.delay(0)).subscribe(print, print, print)
    add_hub('127.0.0.1', 1881)
    return


def add_hub(host, port):
    hubs[(host, port)] = {}
    # will reconnect on its own:
    run(Rx.create(p(produce, h=host, p=port)).pipe(rx.delay(0)))


def send(ws, d):
    d['sid'] = ws.sid
    d['cid'] = cid
    ws.send(js(d))


reg = lambda s: re.compile(r'<%s>(.*)</%s>' % (s, s), re.MULTILINE)
re_name = reg('Name')
re_value = reg('Value')


def xmlval(name, s):
    try:
        return cast(s.split('<%s>' % name, 1)[1].split('</', 1)[0].strip())
    except Exception:
        return ''


def cast(s):
    try:
        return int(s)
    except Exception:
        return s


Funcs = {}


def parse_pkg(cls, prefix):
    for k in dir(cls):
        kp = ('' if not prefix else prefix + ':') + k
        if k.startswith('_'):
            continue
        v = getattr(cls, k)
        if not callable(v):
            continue
        if isinstance(v, type):
            parse_pkg(v, kp)
            continue
        Funcs[kp] = v


class Functions:
    """packages support, addressed like: TR069:parse_inform"""

    class TR069:
        def parse_inform(payload):
            pvs = []
            for n, m in enumerate(re.finditer(re_name, body)):
                s = m.span()
                pvs.append([body[s[0] + 6 : s[1] - 7], ''])
            for n, m in enumerate(re.finditer(re_value, body)):
                s = m.span()
                pvs[n][1] = cast(body[s[0] + 7 : s[1] - 8])
            pvs = dict(pvs)
            cpeid = pvs.get('Device.DeviceInfo.SerialNumber', '')
            res = {'session': {'dm': pvs, 'cpeid': cpeid}}
            res['cpeid'] = cpeid
            res['event'] = xmlval('EventCode', body)
            # yeah whatever
            res['payload'] = '<InformResponse>%s</InformResponse>' % cpeid

            return res

        def classify_cpe(payload, ctx):
            breakpoint()  # FIXME BREAKPOINT

        def authenticate(payload, ctx):
            breakpoint()  # FIXME BREAKPOINT

        def sb_workflows(payload, ctx):
            breakpoint()  # FIXME BREAKPOINT

        def classify_cpe(payload, ctx):
            breakpoint()  # FIXME BREAKPOINT


parse_pkg(Functions, prefix='')

if __name__ == '__main__':
    sys.argv.append('ax-op.nb01')
    main(sys.argv[1])


#     server, port = '127.0.0.1', 1880
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp(
#         'ws://%s:%s/ws/hub' % (server, port),
#         on_message=on_message,
#         on_error=on_error,
#         on_close=on_close,
#     )
#     ws.on_open = on_open
#     ws.run_forever()
