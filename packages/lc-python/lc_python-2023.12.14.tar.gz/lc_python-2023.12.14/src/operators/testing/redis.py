"""
Erradicating the need to start redis server for pytests.

Usage:

On test module level, e.g. test_con_redis.py:
    
from operators.testing.redis import get_redis_exe, setup_redis_con, stop_redis

if not get_redis_exe():
    pytestmark = pytest.mark.skip()


def setup_module(module):
    setup_redis_con('tst_redis')


def teardown_module(module):
    stop_redis()


Or:



pytestmark = pytest.mark.skip() if not get_redis_exe() else pytest.mark.redistest
setup_module = lambda _: setup_redis_con('tst_redis')
teardown_module = lambda _: stop_redis()
"""


import os
import testing.redis
from devapp.tools import Pytest, project
from operators.con import redis, connections, con

redis_servers = {'exe': None, 'cons': {}, 'cur': None}


def get_redis_exe():
    fn = project.root() + '/bin/redis-server'
    p = os.popen('source "%s" && echo $path' % fn).read().strip()
    p = p + '/redis-server'
    exe = p if os.path.exists(p) else os.popen('which redis-server').read().strip()
    redis_servers['exe'] = exe
    return exe


def setup_redis_con(name='redis'):
    exe = redis_servers.get('exe') or get_redis_exe()
    if exe is None:
        # called not at module level, this should fail w/o redis:
        from devapp.app import app

        app.die('Require redis-server binary')
    redis_servers['cur'] = name
    m = redis_servers['cons'].setdefault(name, {})
    if m:
        return
    m['server'] = s = testing.redis.RedisServer(redis_server=exe)
    m['port'] = p = s.dsn()['port']
    dub = connections.add_connection(redis.redis, name)
    dub.con_defaults.port = p
    Pytest.init()


def stop_redis():
    s = redis_servers['cons'].get(redis_servers['cur'])
    if s and s.get('server'):
        s['server'].stop()
