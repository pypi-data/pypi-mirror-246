"""
Project Specific Functions

Note: This file won't be overwritten at ops project re-inits.
"""
import json
import os
import signal
import sys

import jwt
from devapp.app import FLG
from devapp.tools import project, read_file, write_file
from operators.con import add_connection, http, redis
from operators.core import ax_core_ops

# TODO: real db:
# fn_state = os.path.abspath('data/state.json')
# S = json.loads(read_file(fn_state, '{}'))


# def signal_handler(signum, frame):
#     signal.signal(signum, signal.SIG_IGN)  # ignore additional signals
#     write_file(fn_state, json.dumps(S, default=str))
#     sys.exit(0)


# signal.signal(signal.SIGINT, signal_handler)

add_connection(http.http, 'http', streaming=False)
redis = add_connection(redis.redis, 'redis')


class cache:
    boostrap_script = None


here = os.path.abspath(os.path.dirname(__file__))
fn_boostrap_script = here + '/assets/http/client_bootstrap.py'


def hint(msg, schema):
    return [msg, {'schema': schema}]


"""required field"""
req = lambda *a, **kw: field(*a, required=True, **kw)
dfl = lambda *a, **kw: field(*a, required=False, **kw)


def field(v, *a, **kw):
    ri = {'example': v, 'type': type(v).__name__}
    ri.update(kw)
    if a:
        ri['args'] = a
    return ri


g = lambda o, k, d=None: getattr(o, k, d)


def status(s, msg=''):
    if isinstance(msg, dict):
        return {s: msg}
    return 'Status %s%s' % (s, msg)


fn_depl = lambda: project.root() + '/conf/deployments.json'


def get_deployments(c=[0]):
    if not c[0]:
        c[0] = json.loads(read_file(fn_depl(), '{}'))
    return c[0]


class deployment:
    class deployment:
        id = True

        def get(deployment=None, **kw):
            all = get_deployments()
            if not deployment:
                return all
            return all.get(deployment)

        def post(deployment=None, **kw):
            if not deployment:
                return status(403, {'schema error': 'require deployment name'})
            body = kw['body']
            body['pth'] = '/api/bootstrap'
            t = jwt.encode(body, FLG.http_token_secret).decode('utf-8')
            user = body.get('user', '<user>')
            host = body.get('host', '<host>')
            bu = 'https://axc2.axiros.com/lc-deploy/'
            url = body.get('url', bu)
            ic = f'''wget --header 'X-Ax-Api-Token: %s' '{url}api%s' -O - | python'''
            # ic = f"ssh -A {user}@{host} wget --header 'X-Ax-Api-Token: %s' '{url}api%s' -O - | python"
            ic = ic % (t, '/bootstrap')
            return {'token': t, 'claims': body, 'inst': ic}


class token:
    class token:
        def get(headers, **kw):
            return {'claims': headers['claims']}

        def post(
            body,
            headers,
            api=hint(
                'Generates a client token based on what you post',
                schema={
                    'pth': req('/project/my-project/nodes'),
                    'verbs': req(['*'], other=['get', 'head']),
                    'email': req('foo@bar.de'),
                },
            ),
            **kw,
        ):
            pth, verbs, mail = body.get('pth'), body.get('verbs'), body.get('email')
            if not (pth and verbs and mail) or not '@' in mail:
                return status(403, {'schema error': api})
            mine = headers['claims']

            if not pth.startswith(mine['pth']):
                return status(401, 'insufficient perms')
            # TODO check i have get, can i gen a post

            return {
                'token': jwt.encode(body, FLG.http_token_secret).decode('utf-8'),
                'claims': body,
            }


class Functions(ax_core_ops):
    """Custom Project Functions and Config"""

    class api(token):
        def dispatch(data, msg):
            p = data['path'][1:].split('/')
            parent = Functions.api
            while p:
                part = p.pop(0)
                if not part:
                    continue
                f = g(parent, part)
                if f:
                    parent = f
                    continue
                if g(parent, 'id'):
                    data[parent.__name__] = part
            func = parent
            if isinstance(func, type):
                func = g(func, data['headers']['verb'].lower())
            if not func:
                return status(404)

            return func(**data)

        def get(**kw):
            return 'Axiros Low Code Project Mgmt API'

        def bootstrap(**data):
            bs = cache.boostrap_script
            if not bs:
                bs = cache.boostrap_script = read_file(fn_boostrap_script)
            return bs

        class project(token, deployment):
            id = True

            def post(
                data,
                api=hint(
                    'Upload project information',
                    schema={
                        'project': req('lc-wifi-demo'),
                        'mode': dfl('dev', opts=['dev', 'prod']),
                    },
                ),
            ):
                if not data['body']:
                    return ap
