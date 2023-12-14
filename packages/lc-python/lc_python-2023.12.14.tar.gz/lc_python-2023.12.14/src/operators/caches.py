"""
Object Caches


"""
from lru import LRUCache

caches = {}


def process_cache(name='default_process'):
    r = caches.get(name)
    if not r:
        # no lock, we are gevent
        caches[name] = r = Process.dflt(name)
    return r


class Process:
    class lru:
        """engineered for threaded envs"""

        _c = None

        def __init__(self, name='obj_lru_cache', size=1000):
            self._c = caches[name] = LRUCache(size)

        def put(self, id, d):
            self._c.put(id, d)

        def get(self, id):
            return self._c.get(id)

        def pop(self, id):
            r = self._c.get(id)
            if r:
                self._c.invalidate(id)
            return r

    class dflt:
        """
        we are in gevent and don't need all the locking stuffs of lru
        size checking we'll do roughly as in axess sessions (check every...)
        (then with ts)
        """

        _c = None
        name = None

        def __init__(self, name='obj_cache', size=100000):
            self._c = {}
            self.name = name

        def __str__(self):
            return 'Cache %s: %s...' % (self.name, str(self._c)[10000])

        __repr__ = __str__

        def put(self, id, d):
            try:
                h = self._c[id]
                h.update(d)
            except Exception:
                self._c[id] = d

        def get(self, id):
            return self._c.get(id)

        def pop(self, id):
            r = self._c.get(id)
            if r:
                del self._c[id]
            return r
