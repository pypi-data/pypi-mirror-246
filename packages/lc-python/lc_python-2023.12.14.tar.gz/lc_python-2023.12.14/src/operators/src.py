import time
import sys


# FIXME: We need a universal contract regarding stoppage after reconfig or program stop
# e.g. max blocking is 0.1 secs then always we check if a reconfig flag ist set and stop


def interval(count=-1, interval=1, start_delay=0):
    """Interval, start_delay in secs"""
    if start_delay:
        time.sleep(start_delay)
    nr = -1
    if count == 0:
        return
    if count < 0:
        count = sys.maxsize  # 2 Trillion years or so with 1ms interv

    while True:
        nr += 1
        if nr > count:
            return
        yield nr
        time.sleep(interval)


def hello_server(name='world', count=1, interval=1, start_delay=0):
    """Hello World Test Source - a cold observable"""
    if start_delay:
        time.sleep(start_delay)
    for i in range(count):
        # print('i', i, interval)
        yield 'Hello %s, from ax:hello_server! [%s]' % (name, i)
        time.sleep(interval)


# stats = {
#     'data': 0,
#     'err_decode': 0,
#     'server_connects': 0,
#     'err_server': 0,
#     'batches': 0,
#     'dt': {},
#     'sockets': 0,
# }


#         s = stats['dt'].get(addr)
#         if not s:
#             stats['dt'][addr] = s = [0, 0]

#         try:
#             v = json.loads(line)
#             if not 'id' in v:
#                 continue
#         except Exception as ex:
#             stats['err_decode'] += 1
#             s[1] += 1
#             continue

#         if line.strip().lower() == b'quit':
#             break
#         # socket.sendall(line)
#         stats['data'] += 1
#         s[0] += 1
#         m = v.setdefault('sender', {})
#         m['addr'] = addr
#         v['ts'] = v.get('ts') or now()
#         observer.on_next(v)
