"""
Control server interface

🟣 $HOME/repos/ax/devapps/lc-python/docs/dev/devnotes/ctrl.md
"""


import json
import time
from uuid import uuid4

from functools import partial
import gevent
import requests
import rx as Rx
from devapp.app import app
from rx import operators as rx
from rx.scheduler.eventloop import GEventScheduler
from bottle import request, response
from operators.con import add_connection, con, http

GS = GEventScheduler(gevent)
http_cls: http.http = add_connection(http.http, 'http_ctrl', req_conf=True)


def feed_sender(jobmsg, p):
    http_cls.send(p, jobmsg)


def check_done(jobmsg):
    """run at each done msg and job response. clears the S.jobs, flushes response"""
    c = jobmsg['ctrl']
    all = len(c['hub_clients'])
    if all == len(c['done_clients']):
        if all:
            close(jobmsg, {'workers': all})


def close(jobmsg, content):
    j = S.jobs_by_sid.pop(jobmsg['payload']['sid'], 0)
    if j:
        http_cls.respond(content, jobmsg)


def feed_senders(msg):
    c = msg['ctrl']
    senders = msg.get('ctrl.subs', c['sid'])
    # if len(sids) > 1: breakpoint()  # FIXME BREAKPOINT
    p = {c['worker']: msg['payload']}
    e = c.get('err')
    sc = 200
    if e:
        sc = 500
        p['🟥 ERROR'] = e
    for sid in senders:
        jobmsg = S.jobs_by_sid.get(sid)
        if not jobmsg:
            continue
        jobmsg['status_code'] = sc
        feed_sender(jobmsg, p)
        if sc > 299:
            close(jobmsg, {})
            continue
        if not c.get('done'):
            continue
        sck = c.get('hub_sck_name')
        jobmsg['ctrl']['done_clients'][sck] = True
        check_done(jobmsg)


class S:
    stream = None
    channel = None
    me = str(uuid4())
    jobs_by_sid = {}


def is_for_me(msg):
    try:
        return msg['ctrl']['sid']
    except Exception:
        return


def start_listening():
    S.channel = chan = getattr(con, 'redis', 0)
    if not chan:
        hint = 'currently only con.redis supported - please define a redis connection named "redis"'
        return app.die('No channel to listen for ctrl messages', hint=hint)
    S.stream = s = Rx.create(lambda o, _: S.channel.src(o, name='ctrl')).pipe(
        rx.subscribe_on(GS),
        rx.filter(is_for_me),  # there *may* be >1 control clients in the system.
        rx.map(feed_senders),
    )
    s.subscribe(lambda _: 0)


def socket_closed(sid):
    msg = S.jobs_by_sid.pop(sid, 0)
    if not msg:
        return
    hub = msg['ctrl'].get('hub')
    if hub:
        p = msg['payload'].get('path')
        if p:
            msg['payload']['path'] = p.replace('start', 'stop')
            server._send_job_to_specific_hub(hub, msg)


def show_help(msg):
    from devapp.tools import api

    from operators.ctrl.client import API

    r = api.inspect_api(API)
    http_cls.respond(r, msg)


class server:
    def _send_job_to_specific_hub(hub, msg):
        p = msg['payload']
        p['query'].update(p.pop('body', 0) or {})
        p['path'] = h = p['path'].rsplit('/v1/', 1)[-1]
        if 'help' in h:
            return show_help(msg)

        url = f'http://{hub}/api/v1/broadcast'
        res = requests.post(url, data=json.dumps(msg['payload']))
        res = json.loads(res.text)
        msg['ctrl']['hub_clients'].update(res['hub_clients'])
        msg['ctrl']['hub'] = hub

        check_done(msg)

    def job_to_hub(job, msg):
        job['sender'] = S.me
        job['sid'] = sid = msg['_ids']['msg']
        if not S.stream:
            start_listening()
        msg['ctrl'] = {'hub_clients': {}, 'done_clients': {}}
        request.socket_closed_cb = partial(socket_closed, sid=sid)
        S.jobs_by_sid[sid] = msg
        from node_red import nrclient

        hubs = nrclient.get_hubs_list()
        for h in hubs:
            try:
                return server._send_job_to_specific_hub(h, msg)
            except Exception as ex:
                app.error('No hub live', tried=hubs, exc=str(ex))
