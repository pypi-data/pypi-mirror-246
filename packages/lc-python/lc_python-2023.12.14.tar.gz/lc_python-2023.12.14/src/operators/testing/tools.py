import time

from devapp.app import app, init_app_parse_flags
from devapp.tools import FLG, Pytest
from node_red.nr_config_builder import ax_op, get_clean_snk
from node_red.nr_config_builder import nr_config, escaped_flow
from operators.build import ax_pipelines as axp
from operators.build import build_pipelines as build
from operators.build import subscribe_many as subscr

import os, json, sys
from functools import partial

# from operators.doc import add_docu, test_func_doc


# def docu(msg, **kw):
#     app.info(msg, **kw)
#     add_docu(msg, **kw)


def on_demand(name='mydata', **kw):
    return ax_op('ax.src.on_demand', name=name, typ='ax-src', **kw)


def push(data, name='mydata', wait=None):
    from operators.core import ax_core_ops

    r = ax_core_ops.src.named_subjects[name].on_next((data, (0, 0)))
    if wait:
        time.sleep(wait)
    return r


def mem(**kw):
    kw['id'] = kw.get('id', 'memsnk')
    return ax_op('ax.snk.mem', typ='ax-snk', **kw)


# ---------------------------- print
def printflow_nr_esacped(f):
    pf = os.environ.get('printflow').split(':', 1)
    fn = pf[1] if len(pf) > 1 else None
    r = escaped_flow(f)
    r = json.dumps(r)
    if fn:
        with open(fn, 'w') as fd:
            fd.write(r)
        app.warn('Have written', file=fn)
    return r


def exit_on_env_printflow_set(f):
    printflow = os.environ.get('printflow')
    if not printflow:
        return

    # nr_esacped has options in it:
    mode = printflow.split(':', 1)[0]
    jd = {
        'compr': json.dumps,
        'NR': printflow_nr_esacped,
        'default': partial(json.dumps, indent=2),
    }
    print(jd.get(mode, jd.get('default'))(f))
    sys.exit(0)


def build_flow(f, pre=None, build_kw=None, cfg_kw=None, subs_kw=None, **kw):
    """
    tool which all tests need
    """
    init_app_parse_flags('testmode')  # sets the name
    print('')
    app.warn('-' * 80)
    app.warn(Pytest.this_test())
    app.warn('-' * 80)
    if isinstance(f, list):
        last_op_id = f[0].get('id')
        if not last_op_id:
            last_op_id = f[0]['id'] = 'first-op'

    subscr(mode='unsubscribed')
    time.sleep(0)
    # t0 = time.time()
    if pre:
        # FIXME: 0.15 seconds(!) with empty F!
        pre()
    # print(time.time() - t0)

    build_kw = build_kw or {}
    build_kw.update({k[6:]: kw[k] for k in kw if k.startswith('build_')})
    cfg_kw = cfg_kw or {}
    subs_kw = subs_kw or {}
    # build the full flow from the shortcut definition, adding tab, x,y,and nr io config:
    cfg_kw['get_infunc_dflt_opid'] = True
    f, in_id = nr_config(f, **cfg_kw)
    exit_on_env_printflow_set(f)

    # build the pipelines:
    build(f, **build_kw)
    # test_func_doc(graph=[])
    # get access to the mem snk:
    clean_mem_sink = get_clean_snk()
    # subscribe to all pipes:
    subscr(**subs_kw)

    # allow easy simulation of ingress data from node red, next-ing to this subject:
    nr_in = axp.get('nr_sources', {}).get(in_id)
    return clean_mem_sink, nr_in


def huge_data_list(count, counter='id', call=None):
    r = []
    for i in range(count):
        d = huge_data()
        if call:
            call(d, i)
        if counter:
            d[counter] = i
        r.append(d)
    return r


huge_data = lambda: {
    'last_scan_ts': 1550608284151,
    'region': 'ES-SE',
    'WiFi': {
        'NeighboringWiFiDiagnostic': {
            '1': {
                'DiagnosticsInterval': 86400,
                'DiagnosticsState': 'Completed',
                'ResultNumberOfEntries': 4,
            },
            'coll_dt': 2947,
            '5': {
                'DiagnosticsInterval': 86400,
                'DiagnosticsState': 'Completed',
                'ResultNumberOfEntries': 7,
            },
            'Result': {
                '11': {
                    'SecurityModeEnabled': 'WPA2',
                    'Noise': -91,
                    'OperatingChannelBandwidth': '20',
                    'SSID': 'MOVISTAR_EF84',
                    'OperatingFrequencyBand': '2.4GHz',
                    'OperatingStandards': '802.11b/g/n',
                    'auto_channel': -1,
                    'SignalStrength': -55,
                    'type': 'A',
                    'Channel': 6,
                },
                '10': {
                    'SignalStrength': -64,
                    'Noise': -87,
                    'OperatingChannelBandwidth': '20',
                    'SSID': 'DIGAMAX_27',
                    'OperatingFrequencyBand': '2.4GHz',
                    'OperatingStandards': '802.11b/g/n',
                    'auto_channel': -1,
                    'SecurityModeEnabled': 'WPA2',
                    'type': 'A',
                    'Channel': 1,
                },
                '1': {
                    'SecurityModeEnabled': 'WPA2-PSK-CCMP',
                    'Noise': 0,
                    'OperatingChannelBandwidth': '80MHz',
                    'SSID': 'MiFibra-6E405gh',
                    'OperatingFrequencyBand': '5GHz',
                    'OperatingStandards': '802.11a/n/ac',
                    'auto_channel': -1,
                    'SignalStrength': -84,
                    'type': 'A',
                    'Channel': 36,
                },
                '3': {
                    'SignalStrength': -84,
                    'Noise': 0,
                    'OperatingChannelBandwidth': '80MHz',
                    'SSID': 'MOVISTAR_PLUS_A6AA',
                    'OperatingFrequencyBand': '5GHz',
                    'OperatingStandards': '802.11a/n/ac',
                    'auto_channel': -1,
                    'SecurityModeEnabled': 'WPA2-PSK-CCMP',
                    'type': 'A',
                    'Channel': 36,
                },
                '2': {
                    'SecurityModeEnabled': 'WPA2-PSK-CCMP',
                    'Noise': 0,
                    'OperatingChannelBandwidth': '80MHz',
                    'SSID': 'MOVISTAR_A6AA',
                    'OperatingFrequencyBand': '5GHz',
                    'OperatingStandards': '802.11a/n/ac',
                    'auto_channel': -1,
                    'SignalStrength': -84,
                    'type': 'A',
                    'Channel': 36,
                },
                '5': {
                    'SecurityModeEnabled': 'WPA2-PSK-CCMP',
                    'Noise': 0,
                    'OperatingChannelBandwidth': '80MHz',
                    'SSID': 'MOVISTAR_PLUS_FDCA',
                    'OperatingFrequencyBand': '5GHz',
                    'OperatingStandards': '802.11a/n/ac',
                    'auto_channel': -1,
                    'SignalStrength': -84,
                    'type': 'A',
                    'Channel': 52,
                },
                '4': {
                    'SecurityModeEnabled': 'WPA2-PSK-CCMP',
                    'Noise': 0,
                    'OperatingChannelBandwidth': '80MHz',
                    'SSID': 'MOVISTAR_FDCA',
                    'OperatingFrequencyBand': '5GHz',
                    'OperatingStandards': '802.11a/n/ac',
                    'auto_channel': -1,
                    'SignalStrength': -84,
                    'type': 'A',
                    'Channel': 52,
                },
                '7': {
                    'SecurityModeEnabled': 'WPA2-PSK-CCMP',
                    'Noise': 0,
                    'OperatingChannelBandwidth': '80MHz',
                    'SSID': 'MOVISTAR_PLUS_E216',
                    'OperatingFrequencyBand': '5GHz',
                    'OperatingStandards': '802.11a/n/ac',
                    'auto_channel': -1,
                    'SignalStrength': -84,
                    'type': 'A',
                    'Channel': 112,
                },
                '6': {
                    'SecurityModeEnabled': 'WPA2-PSK-CCMP',
                    'Noise': 0,
                    'OperatingChannelBandwidth': '80MHz',
                    'SSID': 'MOVISTAR_E216',
                    'OperatingFrequencyBand': '5GHz',
                    'OperatingStandards': '802.11a/n/ac',
                    'auto_channel': -1,
                    'SignalStrength': -84,
                    'type': 'A',
                    'Channel': 112,
                },
                '9': {
                    'SecurityModeEnabled': 'WPA/WPA2',
                    'Noise': -91,
                    'OperatingChannelBandwidth': '20',
                    'SSID': 'MIPC_NOMAP2.4G',
                    'OperatingFrequencyBand': '2.4GHz',
                    'OperatingStandards': '802.11b/g/n',
                    'auto_channel': -1,
                    'SignalStrength': -75,
                    'type': 'A',
                    'Channel': 4,
                },
                '8': {
                    'SecurityModeEnabled': 'WPA2',
                    'Noise': -88,
                    'OperatingChannelBandwidth': '20',
                    'SSID': 'MiFibra-6E40',
                    'OperatingFrequencyBand': '2.4GHz',
                    'OperatingStandards': '802.11b/g/n',
                    'auto_channel': -1,
                    'SignalStrength': -68,
                    'type': 'A',
                    'Channel': 11,
                },
            },
        },
        'Radio': {
            '1': {
                'Status': 'Up',
                'Enable': 1,
                'OperatingChannelBandwidth': 'Auto',
                'OperatingFrequencyBand': '2.4GHz',
                'OperatingStandards': 'b,g,n',
                'AutoChannelEnable': 1,
                'Stats': {
                    'Noise': -89,
                    'BytesReceived': 3363836,
                    'ErrorsSent': 22,
                    'PacketsReceived': 20722,
                    'ErrorsReceived': 0,
                    'BytesSent': 52579612,
                    'PacketsSent': 120433,
                },
                'Channel': 8,
            },
            'wifi_fingerprint': [
                '78-81-02-70-A8-91_8_vodafoneA890',
                '78-81-02-70-A8-91_112_vodafoneA890_5G',
            ],
            '5': {
                'Status': 'Up',
                'Enable': 1,
                'OperatingChannelBandwidth': 'Auto',
                'OperatingFrequencyBand': '5GHz',
                'OperatingStandards': 'n,ac',
                'AutoChannelEnable': 1,
                'Stats': {
                    'Noise': -89,
                    'BytesReceived': 2252177714,
                    'ErrorsSent': 0,
                    'PacketsReceived': 5819841,
                    'ErrorsReceived': 1,
                    'BytesSent': 1763392521,
                    'PacketsSent': 8495431,
                },
                'Channel': 112,
            },
        },
        'SSID': {
            '1': {
                'LowerLayers': 'Device.WiFi.Radio.1',
                'SSID': 'vodafoneA890',
                'BSSID': '78-81-02-70-A8-91',
            },
            '5': {
                'LowerLayers': 'Device.WiFi.Radio.5',
                'SSID': 'vodafoneA890_5G',
                'BSSID': '78-81-02-70-A8-91',
            },
        },
        'AccessPoint': {
            '1': {
                'Security': {
                    'ModeEnabled': 'PSKAuthentication',
                    'EncryptionMode': 'AESEncryption',
                },
                'SSIDAdvertisementEnabled': 1,
                'SSIDReference': 'Device.WiFi.SSID.1',
            },
            '5': {
                'Security': {
                    'ModeEnabled': 'PSKAuthentication',
                    'EncryptionMode': 'AESEncryption',
                },
                'SSIDAdvertisementEnabled': 1,
                'AssociatedDevice': {
                    '1': {
                        'SignalStrength': -51,
                        'LastDataUplinkRate': 24084819,
                        'MACAddress': '58-C9-35-1C-C7-50',
                        'Hostname': 'New-Host',
                        'OperatingStandard': 'a,n',
                        'AssociationTime': 5751,
                        'LastDataDownlinkRate': 3271205,
                        'Active': 1,
                        'Retransmissions': 0,
                    },
                    '2': {
                        'MACAddress': 'BC-E1-43-8D-63-6E',
                        'LastDataUplinkRate': 180833347,
                        'SignalStrength': -57,
                        'Hostname': 'iPhone-de-Laura',
                        'OperatingStandard': 'ac',
                        'AssociationTime': 5710,
                        'LastDataDownlinkRate': 17681574,
                        'Active': 1,
                        'Retransmissions': 0,
                    },
                },
                'SSIDReference': 'Device.WiFi.SSID.5',
            },
        },
    },
    'DeviceInfo': {
        'ProcessStatus': {'CPUUsage': 3},
        'UpTime': 511440,
        'SerialNumber': 'E1728BXKA29518-0',
        'ModelName': 'Vodafone-H-500-s',
        'MemoryStatus': {'Total': 122852, 'Free': 46496},
        'SoftwareVersion': 'Vodafone-H-500-s-v3.4.20',
        'ManufacturerOUI': '000E8F',
        'ProductClass': 'Vodafone-H-500-s',
        'HardwareVersion': 'Vodafone-H-500-sv1',
        'Manufacturer': 'SERCOMM',
    },
    'ts': 1589538949,
    'Hosts': {
        'Host': {
            '1': {'Active': 1, 'IPAddress': '192.168.0.156'},
            '3': {'Active': 1, 'IPAddress': '192.168.0.159'},
            '2': {'Active': 1, 'IPAddress': '192.168.0.154'},
            '5': {'Active': 1, 'IPAddress': '192.168.0.155'},
            '4': {'Active': 1, 'IPAddress': '192.168.0.157'},
        }
    },
    'collector': {'msg': 'Full Scan', 'code': 200},
    'id': '000E8F-E1728BXKA29518-0',
    'metadata': {'service_id': 'VFH1087112269'},
    'sender': {
        'ip': '10.168.16.19',
        'port': 36224,
        'hostname': 'QTWESPROC02',
        'pid': 32420,
        'ts': 1550449198,
    },
}
