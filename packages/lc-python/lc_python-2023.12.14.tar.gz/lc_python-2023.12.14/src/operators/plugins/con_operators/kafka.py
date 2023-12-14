"""
Kafka Operations
"""
import socket

# from devapp import gevent_patched
from threading import Thread, current_thread
import importlib
import concurrent
import devapp
import sys
from confluent_kafka.admin import (
    AdminClient,
    NewTopic,
    ConfigResource,
)
import time
import confluent_kafka
import gevent
import json
import os
import pickle

from functools import partial
from devapp.app import run_app, do, app
from devapp.tools import FLG, dir_of, confirm as conf, cast, memoize
from operators.con.connections import con_params_dict


class Flags:
    autoshort = ''

    class kafka_url:
        d = 'kafka://192.168.29.104:9092?c.sasl.username=axtract&c.sasl.password={kafka_password}'

    class kafka_password:
        d = 'mysecret'

    class kafka_topic:
        d = ''

    class fn_load_gen:
        n = 'location of a load generator module, with a produce method'
        d = './load.py'

    class force:
        d = False

    class verbose_mode:
        d = False

    class Actions:
        class status:
            d = True

            class topic_match:
                n = 'match filter for topics'
                d = ''

        class about:
            """read docs"""

        class topic_delete:
            """remove topic"""

        class topic_add:
            """add topic"""

        class push:
            """push data"""

            class report_every:
                n = 'sec'
                d = 1

            class items:
                d = 1000

            class dt:
                d = 0.0001

        class pull:
            """consume data"""


here = dir_of(__file__)

p = sys.executable, sys.path
counter = [0, 0]   # pushed, delivered


def confirm(msg):
    if FLG.force:
        return
    return conf(msg)


class kafka:

    from confluent_kafka.admin import AdminClient, NewTopic

    def config(hidepw=False):
        u = FLG.kafka_url.format(kafka_password=FLG.kafka_password)
        p = con_params_dict(u, {})
        pw = p['c.sasl.password']
        pw = (pw[:4] + '...') if hidepw else pw
        return {
            'bootstrap.servers': p['netloc'],
            'log.connection.close': False,
            'queue.buffering.max.ms': 100,
            'sasl.mechanisms': 'PLAIN',
            'sasl.password': pw,
            'sasl.username': p['c.sasl.username'],
            'security.protocol': 'sasl_plaintext',
        }

    def admin():
        return AdminClient(kafka.config())

    def producer():
        return confluent_kafka.Producer(kafka.config())

    def cb_delivery(self, msg, topic=''):
        err = msg.error()
        counter[1] += 1
        if err:
            return print('!' * 100, topic, str(err))
        return


admin = memoize(kafka.admin)
producer = memoize(kafka.producer)


class S:
    con = None


def load_gen():
    k = os.path.abspath(FLG.fn_load_gen)
    k = k + ('.py' if not k.endswith('.py') else '')
    app.die('No load gen found', fn=k) if not os.path.exists(k) else 0
    sys.path.insert(0, k.rsplit('/', 1)[0])
    return importlib.import_module(k.rsplit('/', 1)[-1].rsplit('.py', 1)[0])


def topic_list():
    return Action.status(verbose=False)['topics']


def assure_valid_topic(f):
    s = topic_list()
    t = FLG.kafka_topic
    if t not in s:
        return f('topic unknown', topic=t)
    return t


class Action:
    def _pre():
        pass

    def status(verbose=None):
        verbose = FLG.verbose_mode if verbose is None else verbose
        topics = [t for t in admin().list_topics().topics]
        stm = getattr(FLG, 'status_topic_match', '')
        topics = [t for t in topics if stm in t.lower()]
        if verbose and topics:
            t = [ConfigResource(ConfigResource.Type.TOPIC, k) for k in topics]
            fs = admin().describe_configs(t)

            def f(v):
                d = v.result(timeout=1)
                return {k: cast(v.value) for k, v in d.items()}

            topics = {k.name: f(v) for k, v in fs.items()}

        r = {
            'config': kafka.config(hidepw=True),
            'topics': topics,
            'topic_match': stm,
        }
        return r

    def topic_delete():
        t = assure_valid_topic(app.info)
        if not t:
            return
        confirm(f'Really delete topic {t}')
        admin().delete_topics([t])
        return app.warn('deleted', topic=t)

    def topic_add():
        t = FLG.kafka_topic
        s = topic_list()
        if t in s:
            return app.info('topic already present', topic=t)
        admin().create_topics([NewTopic(t, 1, 1)])
        return app.info('created', topic=t)

    def push():
        t = assure_valid_topic(app.die)
        L = load_gen()
        items = FLG.push_items
        app.info('message schema', json=L.produce(nr=0))
        confirm(f'Really push {items} to {t} topic?')
        dt = FLG.push_dt
        rdt = FLG.push_report_every
        T0 = t0 = now()
        C = list(counter)

        def send1000(t=t, L=L, dt=dt):
            print(current_thread())
            for k in range(1000):
                send(t, *L.produce(nr=k))
                time.sleep(dt)

        threads = 20
        for i in range(threads):
            Thread(target=send1000, args=()).start()
        items = 1000 * threads

        # try:
        #     for i in range(items):
        #         if now() - t0 > rdt:
        #             t0 = stats()
        #         send(t, *L.produce(nr=i))
        #         time.sleep(dt)
        # except KeyboardInterrupt:
        #     print('stop queuing')
        # print(f'queued {counter[0]}. waiting for delivery...')

        while True:
            producer().flush(timeout=0.1)
            if counter[0] == items and counter[0] - counter[1] < 2:
                break
            if now() - t0 > rdt:
                t0 = stats()
            time.sleep(0.1)
        DT = now() - T0
        r = {
            'total time': DT,
            'q/sent': counter,
            'rate': counter[1] / DT,
            'gevent': hasattr(gevent, 'socket') and socket.socket == gevent.socket.socket,
        }
        print(r)
        r = input('foo')

    def about():
        do(os.system, f'vi "{here}/docs/kafka.md"')


now = time.time


def stats(c=[0, [0, 0]]):
    n = now()
    dt = n - c[0]
    r = [counter[0] - c[1][0], counter[1] - c[1][1]]
    print(f'\n{counter}. rate: {r}. intv: {round(dt, 3)}s')
    c[0] = n
    c[1] = list(counter)
    return n


def send(topic, id, data):
    print('.', end='', flush=True)
    prod = producer()
    cb = kafka.cb_delivery
    counter[0] += 1
    v = pickle.dumps(data, 2)
    prod.produce(topic, value=v, key=str(id), on_delivery=cb)
    prod.poll(timeout=0.0)


main = partial(run_app, Action, flags=Flags)
# begin_archive
