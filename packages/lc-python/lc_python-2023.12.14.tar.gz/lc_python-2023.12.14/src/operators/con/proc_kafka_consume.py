#!/usr/bin/env python
"""
Since gevent can't block we do it in sep. process:
"""

import json
import os
import sys
import time
from functools import partial

import msgpack


def shallow(d, p):
    return {k[len(p) :]: v for k, v in d.items() if k.startswith(p)}


# content of file handed as sys.argv[1]:
exmpl = json.dumps(
    {
        'topics': ['axwifi_readings'],
        'enc': 'auto',
        'config': {
            'bootstrap.servers': '1.167.209.156:9091',
            'sasl.mechanisms': 'PLAIN',
            'sasl.password': 'xxxG1',
            'sasl.username': 'external',
            'security.protocol': 'sasl_plaintext',
            'session.timeout.ms': 6000,
            'group.id': 'axwifi_from_queue_2',
        },
    }
)

unp = partial(msgpack.unpackb, raw=False)
unpraw = partial(msgpack.unpackb, raw=True)
now = time.time


def stderr(*msg):
    print(' '.join([str(m) for m in msg]), file=sys.stderr)


class test_msg_creator:
    """In order to simulate kafka server we have this

    Testclient must have created a file with the (binary) msgpack msg

    See test_con_kafka
    """

    def __init__(self, cfg):
        self.cfg = cfg

    def close(self):
        return stderr('closing subprocess')

    def poll(self, timeout=0, c=[0, 0]):
        cfg = self.cfg
        c[0] += 1
        if c[0] > cfg.get('test_msg_count', 1):
            time.sleep(1)
            sys.exit(0)
        dt = cfg.get('test_msg_intv', 1)
        if not c[1]:
            with open(cfg['test_msg_fn'], 'rb') as fd:
                s = fd.read()
            try:
                c[1] = json.loads(s)
            except Exception as ex:
                c[1] = unp(s)
        body = c[1]
        body['cpeid'] = str(f'testcpe-{c[0]}')
        body['ts'] = time.time()
        time.sleep(cfg.get('test_msg_dt', 0))
        return self.msg(json.dumps(body).encode('utf-8'))

    class msg:
        def __init__(self, body):
            self.body = body

        def error(self):
            return 0

        def value(self):
            return self.body


def main():
    stderr('Starting up')
    stderr(sys.argv[1])
    fn = 'n.a.'
    args = sys.argv[1]
    if os.path.exists(args):
        fn = args
        with open(fn) as fd:
            args = fd.read()
        # with open('/tmp/kafkaargs', 'w') as fd: fd.write(args)
    args = json.loads(args)
    cfg = shallow(args, 'ext.stream_reader.cfg.')
    if cfg.get('del_cfg') is not False:
        # security, has password:
        os.unlink(fn)
    # set by kafka from $lc_kafka_mock
    fntm = cfg.get('test_msg_fn')
    if fntm:
        C = test_msg_creator(cfg)
    else:
        import confluent_kafka as kafka

        kafka_cfg = shallow(args, 'c.')
        topics = args['topics']
        stderr('listening topics', topics)
        C = kafka.Consumer(kafka_cfg)
        C.subscribe(topics)
    # deserialize = None
    try:
        while True:
            msg = C.poll(timeout=1.0)
            # stderr('.')
            if msg is None:
                continue
            if msg.error():
                stderr('error')
                continue
            try:
                val = msg.value()
                sep = f'lclen:{len(val)}'.ljust(20)
                # may block as long as main proc needs => backpressure no problem
                sys.stdout.buffer.write(sep.encode('utf-8') + val)
                sys.stdout.buffer.flush()
            except Exception as ex:
                stderr('error: [%s] %s' % (time.ctime(), ex))
                # this will make the main proc die as well
                # makes no sense to remain blocking here, when main process is not taking it
                # (i.e. at broken pipe ex)
                break

            # way faster - but reading is the problem:
            # sys.stdout.buffer.write(msg.value())
    except SystemExit:
        pass
    finally:
        stderr('closing')
        C.close()


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print('kafka consumer.\nExample usage:')
        print(__file__ + ' ' + exmpl)
        sys.exit(1)
    main()
