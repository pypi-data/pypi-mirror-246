# FIXME: only for elasticsearch, integrate into devapp.tools:

import binascii
import datetime
import math
import os
import random
import sys
import time as time_lib
import traceback
from functools import partial
from threading import current_thread
from uuid import uuid4

from devapp.tools import FLG

jobid = lambda: str(uuid4()).split('-', 1)[0]
here = os.path.dirname(os.path.abspath(__file__))
OBJ_CACHE = {}
# the big one:
by_cpeid_cache = {}
FLAGS = FLG


def to_url(shorthand):
    shorthand = shorthand.replace('*', '0.0.0.0')
    if shorthand.startswith(':'):
        return 'http://127.0.0.1' + shorthand
    return shorthand


pass_ = lambda ev: None

# all is millis:
now = lambda: int(time_lib.time() * 1000)

U8 = lambda s: s.encode('utf-8') if isinstance(s, str) else s

tn = lambda: current_thread().name


def err_exit(exc):
    print(exc)
    if not 'Keyboard' in str(exc):
        traceback.print_exc(file=sys.stdout)
    # restarted by systemd:
    sys.exit(1)


def ld(ev):
    print('-------DEBUG LD HIT ----------')
    print(str(ev)[:1000])
    print(ev)


def ldd(ev):
    """in stream debugging via .map(ldd)"""
    breakpoint()
    ld(ev)
    breakpoint()
    return ev


def err(exc):
    import traceback, sys

    traceback.print_exc(file=sys.stderr)
    return exc


def into(m, k, v):
    """for list comprehensions and stream lambdas:"""
    m[k] = v
    return m


def deep(m, dflt, *pth, add=False):
    """Access to props in nested dicts / Creating subdicts by *pth

    Switch to create mode a bit crazy, but had no sig possibilit in PY2:
    # thats a py3 feature I miss, have to fix like that:
    if add is set (m, True) we create the path in m

    Example:
    res = {}
    deep((res, True), [], 'post', 'a', 'b').append('fid')
        creates in res dict: {'post': {'a': {'b': []}}}  (i.e. as list)
        and appends 'fid' to it in one go
        create because init True was set

    """
    # m, add = m if isinstance(m, tuple) else (m, False)
    keys = list(pth)
    while True:
        k = keys.pop(0)
        get = m.setdefault if add else m.get
        v = dflt if not keys else {}
        m = get(k, v)
        if not keys:
            return m


def get_by_pth(r, pth, cast=None, dflt=''):
    """
    Say m a nested dict, e.g. m = {'a': {'b': '3'}}
    Then get_by_pth(m, ('a', 'b'), int) = 3
    Dull.
    But it enables us to prepare getters for later m but known pths in advance:

    foo = getter('a', 'b') # see getter below
    foo(m) = 'c'

    """
    for p in pth:
        r = r.get(p)
        if r is None:
            break
    return dflt if r is None else r if cast is None else cast(r)


getter = lambda pth, cast=None, dflt='': partial(
    get_by_pth, pth=pth.split('.'), cast=cast, dflt=dflt
)


if __name__ == '__main__':
    m = {}
    deep(m, [], 'a', 'b', add=True).append('foo')
    print(m)
    from functools import partial

    p = partial(deep, m, 'D', 'A', 'B', add=True)
    a = p('foo', 'bar')
    assert m == {'A': {'B': {'foo': {'bar': 'D'}}}, 'a': {'b': ['foo']}}


# List of characters that may appear in generated passwords.
_PASSWORD_CHARS = '23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghkmnpqrstuvwxyz'


def generate_random_id(length):
    """Generates a random ID.

    Args:
        length: Length of a generated random ID. Must be an even number.

    Returns:
        Generated random ID string.
    """
    assert length % 2 == 0
    return binascii.hexlify(os.urandom(length / 2))


def generate_password():
    """Generates a random password.

    Returns:
        Generated random password string.
    """
    return ''.join(random.choice(_PASSWORD_CHARS) for _ in xrange(12))


def format_timestamp(ts):
    """Formats a timestamp into a string.

    Args:
        ts: Timestamp, the number of seconds from UNIX epoch.

    Returns:
        A formatted string.
    """
    dt = datetime.datetime.utcfromtimestamp(ts)
    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')


def align_timestamp(timestamp, base_timestamp, interval):
    """Aligns |timestamp| to |base_timestamp| plus multiples of |interval|.

    Args:
        timestamp: Timestamp.
        base_timestamp: Timestamp.
        interval: Alignment interval in seconds.
    """
    assert isinstance(base_timestamp, (int, long))
    assert isinstance(interval, (int, long))
    real_delta = timestamp - base_timestamp
    aligned_delta = int(math.floor(real_delta / interval)) * interval
    return base_timestamp + aligned_delta


def load_testdata(name):
    """Loads a test data.

    Args:
        name: Filename.

    Returns:
        A str.
    """
    with open(os.path.join(os.path.dirname(__file__), 'testdata', name)) as f:
        return f.read()


def time():
    """Returns the current time.

    Similar as time.time(), but can be overridden for testing.

    Returns:
        Timestamp.
    """
    if FLAGS.allow_override_time_for_testing:
        override_time = bottle.request.headers.get('X-Override-Time')
        if override_time:
            return float(override_time)
    return time_lib.time()
