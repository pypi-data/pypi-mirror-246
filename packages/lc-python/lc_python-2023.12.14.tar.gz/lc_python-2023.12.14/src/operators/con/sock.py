from devapp.tools import FLG, define_flags, now, partial as p
from operators.ops.tools import rx, rx_operator
from gevent.server import StreamServer
from operators.kv_tools import kv
from node_red.tools import js
from devapp.app import app
import time
import socket
from operators.con.connections import con_params


def receive(sock, address, cfg, on_next=None):
    """
    returns bytes as read from socket

    mode:
    - line_sep (every line is a message, no response)
    - content_length:<cl_start_byte>:<cl_stop_byte>


    """
    mode = cfg['mode']

    # stats['sockets'] += 1
    m = mode.split(':')
    closeable = sock
    if m[0] == 'line_sep':
        # every line is a piece of data
        # using a makefile because we want to use readline()
        rfileobj = closeable = sock.makefile(mode='rb')
        while True:
            line = rfileobj.readline()
            if not line:
                break
            line = line.strip()
            # when we return a 2 tuple the second one will be msg['src']
            if not on_next:
                return line
            on_next(line, address, sock, cfg)
    elif m[0] == 'content_sep':
        # delimiter
        pass

    elif m[0] == 'content_length':
        # e.g. diameter (cl at bytes 1:4)
        start, stop = int(m[1]), int(m[2])
        while True:
            data = sock.recv(stop)
            if not data:
                app.warn('No data on socket', addr=address)
                break
            cl = int.from_bytes(data[start:], 'big') - stop
            data += sock.recv(cl)
            if not on_next:
                return data
            on_next(data, address, sock, cfg)
        # print(len(data))
        # breakpoint()  # FIXME BREAKPOINT

    else:
        breakpoint()  # FIXME BREAKPOINT
        raise Exception('Mode not supported: %s' % mode)
    if on_next:
        return closeable


def socket_in(cls, observer, port=None):
    """A generic TCP server - a hot observable.
    @mode: dictatates how single events are detected.

    """
    d = con_params(cls)
    if port is not None:
        d['port'] = port
    # sw = True if d['switching'] == 'eager' else False

    def on_next(data, address, sock, cfg, observer=observer, sw=d.get('switching')):
        observer.on_next((data, {'addr': address, 'socket': sock}))
        if sw == 'eager':
            time.sleep(0)

    def handler(socket, address, cfg=d):
        receive(socket, address, cfg, on_next=on_next)

    server = StreamServer((d['host'], d['port']), handler)
    app.info('Opening ingress socket', **d)
    try:
        server.serve_forever()
    except KeyboardInterrupt as ex:
        # FIXME: unify that
        raise


def payload(data, msg):
    b = msg.get('binary')
    if b:
        return b
    if isinstance(data, (dict, list)):
        data = js(data)
    return data if isinstance(data, (bytes, bytearray)) else data.encode('utf-8')


def send(data, msg, sock=None):
    """
    Replying on a socket, we are the server
    The socket object is expected in the msg header.

    The payload may be
    - data as {} or [] -> json or bytes or
    - msg['bytes']
    """
    pl = payload(data, msg)

    sock = sock or msg['objs']['src']['socket']
    # c = cache.pop(msg['_ids']['msg'])
    # sock = c['src']['socket']
    try:
        sock.sendall(pl)
    except Exception as ex:
        app.error(
            'Socket not available to send.',
            nfo='join operator required to get server socket ref',
        )
        raise


# def communicate(cls, data, msg, host, port, pth=None, mode='line_sep'):
#    """
#    mode: Receive mode, as in socket_in
#    """
#    # todo stream=True mode (permanent connection, we do as in rx_operator then, Rx.create)
#    try:
#        app.debug('Trying to connect', host=host, port=port)
#        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        sock.connect((host, port))
#        app.info('Connected client socket', host=host, port=port)
#    except Exception as ex:
#        app.warn('Could not connect', host=host, port=port)
#        raise
#    try:
#        send(data, msg, sock)
#        #receive(socket, address, cfg, on_next=on_next)
#        b = receive(soc, (host, port), sock, mode, on_next=None)
#        if not b:
#            raise Exception('no data', host=host, port=port)
#        resp = {'resp': b}
#        if not pth:
#            data.update(resp)
#        else:
#            kv.update(data, msg, pth=pth, **resp)
#    finally:
#        sock.close()


def socket_out(cls, is_rx=True):
    """
    if host and port are NOT given we'll assume the presence of a connection ref,
    i.e. we are a server.

    If you want a stream, i.e. a permanent connection, then deliver the seperator (can be '')


    """
    d = con_params(cls, defaults='con_defaults_snk')
    if d['is_server']:
        return rx_operator(on_next=send)

    # we are a client
    sock = {}
    stream = d['stream']

    def connect(i, cfg=d):
        if sock.get('sock'):
            return
        host, port = cfg['host'], cfg['port']
        try:
            app.debug('Trying to connect', host=host, port=port)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            app.info('Connected client socket', host=host, port=port)
            sock['sock'] = s
        except Exception as ex:
            sock['sock'] = None
            app.warn('Could not connect', host=host, port=port)

    if stream is None:
        setup = None
    else:
        stream = stream if isinstance(stream, bytes) else stream.encode('utf-8')

        def setup(dt_recon=d['dt_recon']):
            from operators.core import ax_core_ops

            rx_interval_immediate = ax_core_ops.rx.interval_immediate
            rx_interval_immediate(dt_recon).pipe(rx.map(connect)).subscribe(lambda x: x)

    def send_as_client(data, msg, cfg=d):
        app.debug('Socket out send', len=len(data))

        data = data if isinstance(data, bytes) else data.encode('utf-8')
        if stream is not None:
            s = sock.get('sock')
            if s:
                s.sendall(data + stream)
            else:
                app.warn('dropping msg - not connected')
        else:
            host, port = cfg['host'], cfg['port']
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                s.sendall(data)
                s.close()
            except Exception as ex:
                app.warn('dropping msg - could not connect')
                raise

    return rx_operator(on_subscription=setup, on_next=send_as_client)


class sock:
    class con_defaults:
        host = '127.0.0.1'
        port = 60000
        mode = 'line_sep'
        switching = 'eager'

    class con_defaults_snk(con_defaults):
        is_server = True
        stream = None  # connected client sockets
        dt_recon = 1000

    src = classmethod(socket_in)
    # com = classmethod(communicate)
    snk = classmethod(socket_out)
