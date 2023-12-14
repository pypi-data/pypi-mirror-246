# --------------------------------------------------------------- I/O encoding/decoding
# pack/unpack are core ops

from devapp.app import app
from node_red.tools import jp, js

# for the pack function:
try:
    import msgpack
except ImportError as ex:
    msgpack = None
    app.warn('No msgpack')
try:
    import ujson
except ImportError as ex:
    import json

    ujson = json
    app.warn('No ujson')
try:
    import lz4.frame
except ImportError as ex:
    lz4 = None
    app.warn('No lz4')


"""
Formats:
1. normal json
2. 00123{"enc": "msgpack:lz4", pl: 232311, _ids...}<pl>
        5                                       123+5
    pl in the example msgpacklz4 encoded
"""

enc_aliases = {'compressed': 'msgpack:lz4'}


def encode_payload(payload, enc='json', as_msg=False):
    # p = ujson.dumps(msgs)
    # t0 = time()
    enc = enc_aliases.get(enc, enc)
    if not enc or 'json' in enc:
        p = ujson.dumps(payload).encode('utf-8')
    elif 'msgpack' in enc:
        p = msgpack.packb(payload, use_bin_type=True, default=str)
    if 'lz4' in enc:
        p = lz4.frame.compress(p)
    if as_msg:
        return {'enc': enc, 'payload': p}
    else:
        return p


def encode_msg(msg, enc=None):
    """
    Called right before sending out of a snk transport, e.g. to NR or Red. streams

    Usually called by snks, before output.

    Remember that we are not in lala land, means the msg header overrules the signature.

    """
    if enc is None:
        enc = 'json'
    enc = enc_aliases.get(enc, enc)
    # msg header overrules sig:
    if not isinstance(msg, dict):
        msg = {'payload': msg}
    pl = msg.pop('payload', None)
    if pl is None:
        if enc == 'json':
            return js(msg), False
        if enc == 'json_flat':
            # flat json only required for redis streams which takes care of encoding
            # in the lib
            return flat_json(msg), False

        pl = msg
        msg = {}

    plenc = msg.get('enc', None)
    plenc = enc_aliases.get(plenc, plenc)
    if plenc is None:
        if enc == 'json':
            # payload not yet encoded, json wanted => go:
            msg['payload'] = pl
            return js(msg), False

    if plenc is None:
        pl = encode_payload(pl, enc=enc)
        msg['enc'] = enc
    # our non json format, which allows arbitrary subformats, incl. compressed ones:
    msg['pll'] = len(pl)
    head = js(msg)
    hs = str(len(head)).zfill(5)
    h = ('%s%s' % (hs, head)).encode('utf-8')
    return h + pl, True


#     breakpoint()  # FIXME BREAKPOINT
#     m = bytes('|%s|%s|' % (enc, len(head)), 'utf-8') + head + pl
#     return m, True


def flat_json(v, ft=(bytes, str, int, float), bn=(bool, type(None))):
    """
    Following the streams flat dict api.

    For bigger datasets consider pack-ing into compressed binary (see tests)
    """
    # TODO:Perf measure this, I guess simply serializeing ALL is way faster
    return dict(
        [
            (
                k,
                v
                if isinstance(v, ft)
                else str(v)
                if isinstance(v, bn)
                else ujson.dumps(v),
            )
            for k, v in v.items()
        ]
    )


def unpack(data):
    """
    Called at ingress, when json decoding fails at on_message callb.
    of the websock
    => I.e. we auto-unpack all packed messages into our default msg ser:
    """
    # ord({) = 123
    # header len:
    hl = int(data[:5])
    endh = 5 + hl
    h = ujson.loads(data[5:endh])
    pll, enc = h.pop('pll'), h.pop('enc')
    pl = data[endh : endh + pll]
    if 'lz4' in enc:
        pl = lz4.frame.decompress(pl)
    if 'msgpack' in enc:
        pl = msgpack.unpackb(pl, strict_map_key=False)
    # if the originally encoded payload was not a full msg, then
    # the heeader is empty now and we return the original payload
    if not h:
        return pl
    # it was a full msg, insert it in:
    h['payload'] = pl
    return h


def decode_msg(data, _js={'{', '[', 123, 91}):
    """
    We got json or binary - otherwise we crash
    123, 91 = b{ and b[ - which jp can handle
    """
    if not data:
        return None
    if data[0] in _js:
        return jp(data)
    return unpack(data)


msg_key = b'_msg_'  # for flat json api (xadd)


def from_flat_json(m):
    """for bigger datasets consider pack-ing into a compressed binary"""
    # in use by redis
    r = {}
    for k, v in m.items():
        if k == msg_key:
            return decode_msg(v)
        k = k.decode('utf-8') if isinstance(k, bytes) else k
        if isinstance(v, bytes):
            v = decode_msg(v)
        r[k] = v
    return r
