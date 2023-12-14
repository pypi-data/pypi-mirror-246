"""
HTTP Source and Sink.

Using bottle / gevent.

Supports:

- jwt auth based on path prefix check
- Streaming Responses
- Async Responses, sent on other greenlets than ingress one
    We follow the best practice given in
    https://bottlepy.org/docs/dev/async.html#event-callbacks

Big Problem was:

- bottle is setting the response attrs as thread local properties into the LocalResponse
- since we want to answer on other greenlets we need to get a hold on them -> put into objs.src
- that works for mutables like headers and cookies
- but not for status_code and status_line, no way to mutate what was stored in req greenlet
-> We patch `def wsgi` and pull those out from the resp headers, allowing to set them anywhere.
"""


from operators.core import src
import os
from io import BytesIO
import json
import sys

# import ujson as json
import time
from time import sleep
from traceback import format_exc, print_exc

import bottle

import gevent
import jwt
from bottle import (
    Bottle,
    _e,
    get,
    html_escape,
    post,
    request,
    response,
    run,
    tob,
    static_file,
)
from devapp.app import app
from devapp.tools import FLG, define_flags, now, process_instance_offset
from devapp.tools import get_deep, partial as p
from operators.con import connections
from operators.const import ax_pipelines
from operators.ops.tools import rx_operator
from gevent.pywsgi import WSGIHandler


class flags:
    autoshort = 's'

    class http_token_secret:
        n = 'Secret to use for any jwt verification'


define_flags(flags)


def wsgi(self, environ, start_response, response=response):
    """The bottle WSGI-interface."""
    # patch: pop status line from the headers list if set:
    try:
        # if he sent chunks TO us, we can, on this interface only assemble
        # i.e. hope it is not an endless stream. For real unbounded streaming TO us
        # (
        if 'chunked' in environ.get('HTTP_TRANSFER_ENCODING', '').lower():
            app.warn(
                'Chunked request on non chunk enabled endpoint. Awaiting whole upstream'
            )
            del environ['HTTP_TRANSFER_ENCODING']
            body = environ['wsgi.input'].read()
            environ['CONTENT_LENGTH'] = len(body)
            environ['wsgi.input'] = BytesIO(body)

        out = self._cast(self._handle(environ))
        # rfc2616 section 4.3
        if (
            response._status_code in (100, 101, 204, 304)
            or environ['REQUEST_METHOD'] == 'HEAD'
        ):
            if hasattr(out, 'close'):
                out.close()
            out = []
        # ---------------- patch ---------------------------------------------:
        sl, hl = None, []
        for k in response.headerlist:
            if k[0] == 'Status-Line':
                sl = k[1]
            else:
                hl.append(k)
        s = start_response(sl or response._status_line, hl)
        # ------------ end patch ---------------------------------------------:
        return out
    except (KeyboardInterrupt, SystemExit, MemoryError):
        raise
    except Exception:
        if not self.catchall:
            raise
        err = '<h1>Critical error while processing request: %s</h1>' % html_escape(
            environ.get('PATH_INFO', '/')
        )
        if FLG.log_level < 20:
            err += (
                '<h2>Error:</h2>\n<pre>\n%s\n</pre>\n'
                '<h2>Traceback:</h2>\n<pre>\n%s\n</pre>\n'
                % (html_escape(repr(_e())), html_escape(format_exc()))
            )
        environ['wsgi.errors'].write(err)
        headers = [('Content-Type', 'text/html; charset=UTF-8')]
        start_response('500 INTERNAL SERVER ERROR', headers, sys.exc_info())
        return [tob(err)]


def run_application(self):
    # allow a request.socket_closed_cb = partial(socket_closed, sid=sid) for ctrl-c at chunk rcv handling:
    assert self.result is None
    try:
        self.result = self.application(self.environ, self.start_response)
        self.process_result()
    except Exception:
        cb = getattr(self.environ['bottle.request'], 'socket_closed_cb', 0)
        if cb:
            cb()

    finally:
        close = getattr(self.result, 'close', None)
        try:
            if close is not None:
                close()
        finally:
            # Discard the result. If it's a generator this can
            # free a lot of hidden resources (if we failed to iterate
            # all the way through it---the frames are automatically
            # cleaned up when StopIteration is raised); but other cases
            # could still free up resources sooner than otherwise.
            close = None
            self.result = None


Bottle.wsgi = wsgi
WSGIHandler.run_application = run_application  # Bottle's Gev Wsgiserver's handler is this


class http:
    server_running = False
    api_endpoints = None

    @classmethod
    def gen_token(cls, data, msg):
        """intended for passing injects into us and return output in debug node"""
        t = jwt.encode(data, FLG.http_token_secret)
        return t

    class con_defaults:
        base_path = '/api'
        host = '0.0.0.0'
        port = 1885
        streaming = False
        token_key = None
        d_assets = None
        port_incr_instance = True

    def _serialize(data):
        return json.dumps(data, default=str).encode('utf-8')

    def push_to_subj(data, msg):
        s = src.named_subjects.get(data['path'])
        if not s:
            return http._err('not implemented', details=data, status_code=501, msg=msg)
        msg['req'] = data  # keep a ref
        d = msg['payload'] = {}
        d['verb'] = data['headers']['verb']
        d['path'] = data['path']

        d.update(data['body'] if data['body'] is not None else data['query'])
        s.on_next(msg)

    @classmethod
    def request(cls, observer, **kw):
        """The main Event Source - starts the server, when there is a subscription"""
        if cls.api_endpoints is None:
            cls.api_endpoints = {}
        d = connections.con_params(cls, observer=observer)
        if not d:
            return
        p = kw.get('port')
        if p:
            kw['port'] = process_instance_offset(kw['port'])
        d.update(kw)
        base_path = d['base_path']
        token_key = d['token_key']  # TODO: X-AX-.. -> X-Ax-...
        streaming = d.get('streaming')
        # d = {'streaming': streaming, 'host': host, 'port': port, 'base_path': base_path}

        def verify_token(path, token_key, headers, _secr=FLG.http_token_secret):
            try:
                claims = jwt.decode(headers.pop(token_key), _secr, algorithms='HS256')
                allowed_pth = claims['pth']
                if not path.startswith(allowed_pth):
                    err = 'Not allowed (only %s)' % allowed_pth
                    raise
                v = headers['verb']
                if v == 'get':
                    return
                allowed_verbs = claims.get('verbs')
                if '*' not in allowed_verbs:
                    if allowed_verbs and v not in allowed_verbs:
                        err = 'Method not allowed (only %s)' % allowed_verbs
                        raise

            except jwt.exceptions.InvalidSignatureError as e:
                response.status = 401
                return str(e)
            except Exception:
                response.status = 401
                err = 'No valid %s' % token_key
                return err
            headers['claims'] = claims

        Q = gevent.queue.Queue
        # def handle_req(pth, cfg=d, obs=observer, token=token):

        if d.get('d_assets') is not None:

            @get(base_path + 'assets/<filepath:path>', name='assets')
            @post(base_path + 'assets/<filepath:path>', name='assets')
            def server_static(filepath, base=d.get('d_assets')):
                return static_file(filepath, root=base)

        @get(base_path + '<pth:path>')
        @post(base_path + '<pth:path>')
        def handle_req(
            pth,
            token_key=token_key,
            base_path=base_path,
            Q=Q,
            obs=observer,
            streaming=streaming,
        ):
            r = request
            # to be overwritten if different
            response.content_type = 'application/json'
            headers = {k: v for k, v in r.headers.items()}
            headers['verb'] = verb = r.method.lower()
            if token_key:
                err = verify_token(base_path + pth, token_key, headers)
                if err:
                    hint = 'Send valid %s. E.g. http <url> %s:<your token>'
                    return http._err(
                        'unauthorized',
                        details={'err': err, 'hint': hint % (token_key, token_key)},
                        status_code=401,
                    )

            d = {
                'path': pth,
                'body': request.json,
                'query': {k: v for k, v in r.query.items()},
                'headers': headers,
            }

            q = Q()
            # app.debug('request', json=d)
            # infos stored in local store at bottle
            # since the response must be sent by this greenlet, but we'll want
            # to set headers and status later, in other greenlets, we must
            # pass the props around, in order to be able to change them
            ra = {k: getattr(response, k) for k in ('_cookies', '_headers', 'body')}
            src = {
                'queue': q,
                'resp': response,
                'respattrs': ra,
                'streaming': streaming,
                # 'greenlet': gevent.getcurrent()
            }
            # push into the stream:
            obs.on_next((d, src))
            return q

        app.info('Starting http request handler.', **d)
        cls.server_running = True
        run(host=d['host'], port=d['port'], server='gevent')

    def await_response(data, msg):
        """Should be defined async on node red, may block"""
        data = http._get_response(msg) or data
        # might block:
        if callable(data):
            return data()
        return data

    def response(is_rx=True):
        """
        Response sender based on ax.src.http requests
        """
        return rx_operator(on_next=http.respond)

    def respond(data, msg, status_code=None, timeout=100):
        """
        The non rx direct snk/operator version

        Can be used also as function or operator, then incl. status_code.

        data Conventions:
          - type str: Return it, as text/plain
          - type dict:
              - has 'text/html', 'text/plain' key: Return this, with mimetype
              - else: Return application/json with all data, json dumps-ed, except told
                differently in msg['src']

        """
        try:
            src = msg['objs']['src']
            resp = src['resp']
        except Exception as _:
            return  # TODO: when does this happen?

        s = msg.get('status_code') or status_code or 200
        ra = src.get('respattrs')
        if ra:
            resp._cookies = ra['_cookies']
            resp._headers = ra['_headers']
            # resp._body = ra['body']
            # this is NOT setting the real response status - but prevents crashing
            resp.status = s  # int, not mutable, is set in original greenlet to 200. So:
        ct_is_json = resp.content_type == 'application/json'
        if isinstance(data, str):
            if ct_is_json:
                resp.content_type = 'text/plain'
            d = data
        else:
            d = None
            # two convenience keys for biz funcs (could be done via msg['src'] header as well)
            for k in 'text/html', 'text/plain':
                d = data.get(k)
                if d:
                    resp.content_type = k
                    break

            if d is None:
                if not ct_is_json:
                    d = data.get('body')
                if d is None:
                    # js dumps:
                    resp.content_type = 'application/json'
                    d = http._serialize(data)

        sl = bottle._HTTP_STATUS_LINES
        resp.headers['Status-Line'] = sl.get(s) or '%s Unknown' % s

        q, streaming = http._src(msg)
        if streaming == 2:
            data['_log'] = msg['objs']['src']

        if not streaming or streaming == 2:
            resp.headers['Content-Length'] = len(d)
        cbs = src.get('response_callbacks')
        if cbs:
            [cb() for cb in cbs]
        q.put(d)
        q.put(StopIteration)
        sleep(0)

    def send(data, msg):
        """Stream down a chunk"""
        q, streaming = http._src(msg)
        if not streaming:
            return app.warn('Cannot send', streaming=False)
        if streaming == 2:
            l = msg['objs']['src'].setdefault('sent', ())
            l += ([now(), data],)
        else:
            d = http._serialize(data)
            d += b'\r\n'  # required to actually send the chunk
            # if b'User-Agent' in d: breakpoint()  # FIXME BREAKPOINT
            q.put(d)

    def _add_response(resp_data, msg):
        msg['objs']['src']['response_data'] = resp_data
        return resp_data

    def _add_response_callback(callback, msg):
        msg['objs']['src'].setdefault('response_callbacks', []).append(callback)

    def _get_response(msg):
        try:
            return msg['objs']['src'].get('response_data')
        except Exception as ex:
            return None

    def _err(err_msg, details, status_code=500, msg=None):
        """Helper for unified error payload. When msg is given we set status_code"""
        if msg:
            msg['status_code'] = status_code
        return {'status_code': status_code, 'err': err_msg, 'details': details}

    def _src(msg):
        src = msg['objs']['src']
        return src['queue'], src.get('streaming')


def gen_token():
    claims = {'pth': '/', 'verbs': ['get', 'put', 'post', 'delete', 'head']}
    t = jwt.encode(claims, 'xxx')
    return t
