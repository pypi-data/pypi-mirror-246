#!/usr/bin/env python
"""
"TR-069" client simulator

Sending easy parsable XML with TR-069 session model
"""


import bottle, requests
from bottle import route, run
from functools import partial
import rx
from rx import interval, of, pipe, operators as op


acs = 'http://127.0.0.1:1880/tr069'
port = 8080
host = '127.0.0.1'

cnrpath = '/cnr'

eventcodes = {6: '6 CONNECTION REQUEST', 0: '0 BOOTSTRAP', 1: '1 BOOT', 3: '3 Periodic'}
d = 'Device.'
di = d + 'DeviceInfo.'
ms = d + 'ManagementServer.'
wp = d + 'WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.'
dm = {
    di + 'HardwareVersion': 'hwver123',
    di + 'SoftwareVersion': 'swver123',
    di + 'SoftwareVersion': 'swver123',
    di + 'SerialNumber': 'serial123',
    di + 'SerialNumber': 'serial123',
    ms + 'ConnectionRequestURL': 'http://%s:%s%s' % (host, port, cnrpath),
    ms + 'PeriodicInformInterval': 3600,
    wp + 'ExternalIPAddress': '1.2.3.4',
    wp + 'PPPUserName': 'initial',
}
S = {'insession': False, 'dm': dm, 'event_code': 0}


@route(cnrpath)
def cnr():
    send_inform(event_code=6)
    return ''


def get_job(result=None):
    pass


def xml(d):
    s = []
    pvs = d.pop('pvs')
    for k, v in d.items():
        s += ['<%s>%s</%s>' % (k, v, k)]
    if pvs:
        s += ['<ParameterList>']
        for k, v in pvs.items():
            s += [
                '  <ParameterValueStruct>',
                '    <Name>%s</Name>' % k,
                '    <Value>%s</Value>' % v,
                '  </ParameterValueStruct>',
            ]
        s += ['</ParameterList>']
    return '\n'.join(s)


def send_inform(r):
    s = {'EventCode': eventcodes[0], 'pvs': dict(S['dm'])}
    res = requests.post(acs, data=xml(s), cookies={'someheader': 'someval'})
    print(res.text)
    if not res.status_code < 300 or not 'InformResponse' in res.text:
        print('uncool inform result', res.text, res.status)
        sys.exit(0)
    job = requests.post(acs, data='', cookies=res.cookies)
    breakpoint()  # FIXME BREAKPOINT
    while job.text:
        res = run(job.text)


jobs = {'inform': send_inform}


def is_due(r):
    return False


def cwmp_session(event_code=None):
    of({'job': 'inform'}).pipe(
        op.group_by(lambda j: j['job']),
        op.flat_map(lambda s: s.pipe(op.map(jobs[s.key]))),
        op.expand(lambda result: get_job(result)),
    ).subscribe(print)


periodic = interval(1).pipe(op.filter(is_due), op.map(cwmp_session(6)))

if __name__ == '__main__':
    # periodic.subscribe()
    cwmp_session()
    # run(host='localhost', port=8080, debug=True)
