true = True
false = False
null = False 


def produce(nr):
    #d = {'a': 'b'}
    id = f'id_{nr}'
    d['id'] = id
    return id, d


d = {
    "2": {
        "expert": {
            "algo": "greedy",
            "cur_bw": 20,
            "cur_ch": 11,
            "cur_radio_ch": 11,
            "target_radio_ch": 11,
            "target_ch": 11,
            "target_q": 1,
            "target_bw": "Auto",
            "neighbors": {
                "total": 28,
                "aci": 0,
                "cci": 0,
                "friends": 0,
                "extenders": 0,
                "all": [
                  {
                      "bssid": "C6-FB-E4-F4-FE-6E",
                      "channel": 6,
                      "ssid": "",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -62,
                      "type": "A"
                  },
                    {
                      "bssid": "74-67-F7-3B-D2-02",
                      "channel": 6,
                      "ssid": "",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -71,
                      "type": "A"
                  },
                    {
                      "bssid": "B4-FB-E4-F4-FE-6E",
                      "channel": 6,
                      "ssid": "CMN",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -61,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-14-CC-A8",
                      "channel": 6,
                      "ssid": "EMANGUEST",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -61,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-54-CC-A8",
                      "channel": 6,
                      "ssid": "EMAN2",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -60,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-FB-8D-C8",
                      "channel": 4,
                      "ssid": "GUESTELEA",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -68,
                      "type": "A"
                  },
                    {
                      "bssid": "B6-FB-E4-F4-FE-6E",
                      "channel": 6,
                      "ssid": "CM-N_GUEST",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -61,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-14-CC-48",
                      "channel": 6,
                      "ssid": "EMANGUEST",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -80,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-94-CC-A8",
                      "channel": 6,
                      "ssid": "EMAN8",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -61,
                      "type": "A"
                  },
                    {
                      "bssid": "00-FE-C8-DD-47-91",
                      "channel": 1,
                      "ssid": "O2-Guest",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -88,
                      "type": "A"
                  },
                    {
                      "bssid": "60-31-97-0F-B7-A7",
                      "channel": 1,
                      "ssid": "Axiros",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -46,
                      "type": "A"
                  },
                    {
                      "bssid": "80-8C-97-D8-39-0F",
                      "channel": 1,
                      "ssid": "Internet",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -87,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-14-A0-98",
                      "channel": 1,
                      "ssid": "EMANGUEST",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -57,
                      "type": "A"
                  },
                    {
                      "bssid": "72-31-97-0F-B7-A4",
                      "channel": 1,
                      "ssid": "Axiros_2.4_guest",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -47,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-94-A0-98",
                      "channel": 1,
                      "ssid": "EMAN8",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -57,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-54-A0-98",
                      "channel": 1,
                      "ssid": "EMAN2",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -56,
                      "type": "A"
                  },
                    {
                      "bssid": "90-5C-44-2F-30-61",
                      "channel": 1,
                      "ssid": "&lt;|&gt;",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -87,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-D4-A0-98",
                      "channel": 1,
                      "ssid": "GUESTELEA",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -57,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-3B-8D-C8",
                      "channel": 4,
                      "ssid": "EMANGUEST",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -68,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-94-EE-98",
                      "channel": 1,
                      "ssid": "EMAN8",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -67,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-54-EE-98",
                      "channel": 1,
                      "ssid": "EMAN2",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -67,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-14-EE-98",
                      "channel": 1,
                      "ssid": "EMANGUEST",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -67,
                      "type": "A"
                  },
                    {
                      "bssid": "92-5C-14-2F-30-61",
                      "channel": 1,
                      "ssid": "UPC",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -87,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-D4-F0-E8",
                      "channel": 1,
                      "ssid": "GUESTELEA",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -84,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-D4-EE-98",
                      "channel": 1,
                      "ssid": "GUESTELEA",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -67,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-7B-8D-C8",
                      "channel": 4,
                      "ssid": "EMAN2",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -69,
                      "type": "A"
                  },
                    {
                      "bssid": "BC-99-11-76-13-5D",
                      "channel": 3,
                      "ssid": "Zyxel_135D",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -40,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-BB-8D-C8",
                      "channel": 4,
                      "ssid": "EMAN8",
                      "noise": -70,
                      "bandwidth": 20,
                      "rssi": -69,
                      "type": "A"
                  }
                ]
            },
            "cur_q": 1,
            "delta_q": 0,
            "denied_by_condition": true
        },
        "recommendations": {
            "all": [
                {
                    "subtree": "ssid",
                    "index": "1",
                    "type": "security_mode",
                    "value": "WEP-128"
                },
                {
                    "subtree": "ssid",
                    "index": "1",
                    "type": "security_open_wifi",
                    "value": "No Encryption"
                },
                {
                    "subtree": "ssid",
                    "index": "1",
                    "type": "clients_op_standards",
                    "value": {
                        "00-00-00-00-00-01": "b"
                    }
                }
            ],
            "total": 3,
            "detail": {
                "security_mode": 1,
                "security_open_wifi": 1,
                "clients_op_standards": 1
            },
            "ts": 1673515744.4641435
        },
        "pme": {},
        "changes": {
            "auto": 0,
            "axwifi": 0,
            "manual": 1,
            "owner": "manual",
            "ts": 1673515744.348,
            "auto_last24h": 0,
            "manual_last24h": 0,
            "axwifi_last24h": 0
        },
        "ssid": {
            "1": {
                "clients": {
                    "all": [
                        {
                            "SignalStrength": -80,
                            "OperatingStandard": "b",
                            "LastDataDownlinkRate": 0,
                            "LastDataUplinkRate": 0,
                            "MACAddress": "00-00-00-00-00-01",
                            "AuthenticationState": 1,
                            "vendor": "Officially Xerox",
                            "Active": 1,
                            "ipaddress": "n.a.",
                            "AssociationTime": "n.a.",
                            "Noise": 0,
                            "snr": 0,
                            "HostName": "n.a.",
                            "Retransmissions": 0,
                            "Stats": {
                                "BytesSent": 0,
                                "BytesReceived": 0,
                                "PacketsSent": 0,
                                "PacketsReceived": 0,
                                "ErrorsSent": 0,
                                "ErrorsReceived": 0,
                                "RetransCount": 0
                            }
                        },
                        {
                            "SignalStrength": -50,
                            "OperatingStandard": "n.a.",
                            "LastDataDownlinkRate": 0,
                            "LastDataUplinkRate": 0,
                            "MACAddress": "00-00-00-00-00-00",
                            "AuthenticationState": 1,
                            "vendor": "Officially Xerox",
                            "Active": 1,
                            "ipaddress": "n.a.",
                            "AssociationTime": "n.a.",
                            "Noise": 0,
                            "snr": 0,
                            "HostName": "n.a.",
                            "Retransmissions": 0,
                            "Stats": {
                                "BytesSent": 0,
                                "BytesReceived": 0,
                                "PacketsSent": 0,
                                "PacketsReceived": 0,
                                "ErrorsSent": 0,
                                "ErrorsReceived": 0,
                                "RetransCount": 0
                            }
                        }
                    ],
                    "total": 2,
                    "good_rssi_macs": [
                        "00-00-00-00-00-00"
                    ],
                    "good_rssi": 1,
                    "low_rssi_macs": [
                        "00-00-00-00-00-01"
                    ],
                    "low_rssi": 1,
                    "i1_rssi_macs": [],
                    "i1_rssi": 0,
                    "i2_rssi_macs": [
                        "00-00-00-00-00-00"
                    ],
                    "i2_rssi": 1,
                    "i3_rssi_macs": [],
                    "i3_rssi": 0,
                    "i4_rssi_macs": [
                        "00-00-00-00-00-01"
                    ],
                    "i4_rssi": 1,
                    "i5_rssi_macs": [],
                    "i5_rssi": 0,
                    "sig_avg": -65,
                    "intervals": {
                        "i1": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i2": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i3": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i4": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i5": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        }
                    },
                    "global": {
                        "lddr": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "ldur": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "esent": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "erec": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        }
                    },
                    "good": {
                        "lddr": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "ldur": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "esent": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "erec": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        }
                    },
                    "low_rssi_macs_last24h": []
                }
            },
            "2": {
                "clients": {
                    "all": [],
                    "total": 0,
                    "good_rssi_macs": [],
                    "good_rssi": 0,
                    "low_rssi_macs": [],
                    "low_rssi": 0,
                    "i1_rssi_macs": [],
                    "i1_rssi": 0,
                    "i2_rssi_macs": [],
                    "i2_rssi": 0,
                    "i3_rssi_macs": [],
                    "i3_rssi": 0,
                    "i4_rssi_macs": [],
                    "i4_rssi": 0,
                    "i5_rssi_macs": [],
                    "i5_rssi": 0,
                    "sig_avg": 0,
                    "intervals": {
                        "i1": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i2": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i3": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i4": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i5": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        }
                    },
                    "global": {
                        "lddr": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "ldur": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "esent": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "erec": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        }
                    },
                    "good": {
                        "lddr": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "ldur": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "esent": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "erec": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        }
                    }
                }
            }
        },
        "issues": {},
        "Radio": {
            "Status": "Up",
            "Enable": 1,
            "OperatingChannelBandwidth": "20MHz",
            "OperatingFrequencyBand": "2.4GHz",
            "OperatingStandards": "n",
            "RegulatoryDomain": "DE",
            "AutoChannelEnable": 0,
            "PossibleChannels": "1,2,3,4,5,6,7,8,9,10,11,12,13",
            "Channel": 11,
            "TransmitPower": -1,
            "possible_channels": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13
            ],
            "noise": 0,
            "enabled": true,
            "band": "2",
            "radio_chan": 11,
            "bandwidth": 20,
            "op_standard": 4,
            "Stats": {
                "BytesSent": 24,
                "BytesReceived": 22,
                "PacketsSent": 192,
                "PacketsReceived": 176,
                "ErrorsSent": 0,
                "ErrorsReceived": 2
            },
            "upper_channel": 13
        },
        "SSID": {
            "1": {
                "BSSID": "54-83-3A-3B-2E-01",
                "LowerLayers": "Device.WiFi.Radio.1",
                "SSID": "Zyxel_2E01",
                "Stats": {
                    "BytesReceived": 11,
                    "ErrorsSent": 0,
                    "PacketsReceived": 88,
                    "ErrorsReceived": 1,
                    "BytesSent": 12,
                    "PacketsSent": 96
                },
                "Security": {
                    "ModeEnabled": "WEP-128",
                    "EncryptionMode": "None"
                },
                "SSIDAdvertisementEnabled": 1,
                "SSIDReference": "Device.WiFi.SSID.1",
                "AssociatedDevice": {
                    "1": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-00",
                        "SignalStrength": -50,
                        "AuthenticationState": 1,
                        "Type": "Client"
                    },
                    "2": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-01",
                        "SignalStrength": -80,
                        "AuthenticationState": 1,
                        "OperatingStandard": "b",
                        "Type": "Client"
                    }
                },
                "band": "2",
                "rid": "54833A-S190Y20057813"
            },
            "2": {
                "BSSID": "54-83-3A-3B-2E-01",
                "LowerLayers": "Device.WiFi.Radio.1",
                "SSID": "Zyxel_2E01_G",
                "Stats": {
                    "BytesReceived": 11,
                    "ErrorsSent": 0,
                    "PacketsReceived": 88,
                    "ErrorsReceived": 1,
                    "BytesSent": 12,
                    "PacketsSent": 96
                },
                "band": "2",
                "rid": "54833A-S190Y20057813"
            }
        },
        "scan_dt": 3887
    },
    "5": {
        "expert": {
            "algo": "greedy",
            "cur_bw": 80,
            "cur_ch": 42,
            "cur_radio_ch": 36,
            "target_radio_ch": 132,
            "target_ch": 138,
            "target_q": 1,
            "target_bw": 80,
            "neighbors": {
                "total": 28,
                "interfering": 15,
                "friends": 0,
                "extenders": 0,
                "all": [
                  {
                      "bssid": "A0-E4-CB-C9-DB-B5",
                      "channel": 36,
                      "ssid": "filipeO2-Internet-803-5GHz",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -92,
                      "type": "A"
                  },
                    {
                      "bssid": "62-31-97-0F-B7-AD",
                      "channel": 108,
                      "ssid": "",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -42,
                      "type": "A"
                  },
                    {
                      "bssid": "BC-99-11-76-13-5E",
                      "channel": 36,
                      "ssid": "Zyxel_135D_5G",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -40,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-3B-7B-FC",
                      "channel": 44,
                      "ssid": "EMANGUEST",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -71,
                      "type": "A"
                  },
                    {
                      "bssid": "60-31-97-0F-B7-A8",
                      "channel": 108,
                      "ssid": "Axiros_5G",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -43,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-BB-91-0C",
                      "channel": 44,
                      "ssid": "EMAN8",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -78,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-54-CC-AC",
                      "channel": 108,
                      "ssid": "EMAN2",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -61,
                      "type": "A"
                  },
                    {
                      "bssid": "B6-FB-E4-F8-00-17",
                      "channel": 44,
                      "ssid": "CM-N_GUEST",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -87,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-D4-EE-9C",
                      "channel": 100,
                      "ssid": "GUESTELEA",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -63,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-54-EE-9C",
                      "channel": 100,
                      "ssid": "EMAN2",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -63,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-94-EE-9C",
                      "channel": 100,
                      "ssid": "EMAN8",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -63,
                      "type": "A"
                  },
                    {
                      "bssid": "62-31-97-0F-B7-DD",
                      "channel": 52,
                      "ssid": "",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -37,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-14-EE-9C",
                      "channel": 100,
                      "ssid": "EMANGUEST",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -63,
                      "type": "A"
                  },
                    {
                      "bssid": "60-31-97-0F-B7-D8",
                      "channel": 52,
                      "ssid": "BMCOM",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -37,
                      "type": "A"
                  },
                    {
                      "bssid": "B4-FB-E4-F8-00-17",
                      "channel": 44,
                      "ssid": "CMN",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -87,
                      "type": "A"
                  },
                    {
                      "bssid": "C6-FB-E4-F5-FE-6E",
                      "channel": 44,
                      "ssid": "",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -80,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-FB-7B-FC",
                      "channel": 44,
                      "ssid": "GUESTELEA",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -73,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-BB-7B-FC",
                      "channel": 44,
                      "ssid": "EMAN8",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -72,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-D4-CC-AC",
                      "channel": 108,
                      "ssid": "GUESTELEA",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -60,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-94-CC-AC",
                      "channel": 108,
                      "ssid": "EMAN8",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -61,
                      "type": "A"
                  },
                    {
                      "bssid": "C6-FB-E4-F8-00-17",
                      "channel": 44,
                      "ssid": "",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -86,
                      "type": "A"
                  },
                    {
                      "bssid": "B4-FB-E4-F5-FE-6E",
                      "channel": 44,
                      "ssid": "CMN",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -81,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-7B-7B-FC",
                      "channel": 44,
                      "ssid": "EMAN2",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -72,
                      "type": "A"
                  },
                    {
                      "bssid": "62-31-97-0F-B7-A9",
                      "channel": 108,
                      "ssid": "Axiros_5_guest",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -43,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-FB-91-0C",
                      "channel": 44,
                      "ssid": "GUESTELEA",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -78,
                      "type": "A"
                  },
                    {
                      "bssid": "44-1E-98-14-CC-AC",
                      "channel": 108,
                      "ssid": "EMANGUEST",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -61,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-3B-91-0C",
                      "channel": 44,
                      "ssid": "EMANGUEST",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -78,
                      "type": "A"
                  },
                    {
                      "bssid": "34-FA-9F-7B-91-0C",
                      "channel": 44,
                      "ssid": "EMAN2",
                      "noise": -70,
                      "bandwidth": 80,
                      "rssi": -78,
                      "type": "A"
                  }
                ]
            },
            "cur_q": 0.05840818770196917,
            "delta_q": 0.9415918122980308,
            "denied_by_condition": true
        },
        "recommendations": {
            "all": [
                {
                    "subtree": "ssid",
                    "index": "5",
                    "type": "security_encryption",
                    "value": "TKIPEncryption"
                },
                {
                    "subtree": "ssid",
                    "index": "5",
                    "type": "security_mode",
                    "value": "WEP-128"
                },
                {
                    "subtree": "ssid",
                    "index": "5",
                    "type": "security_wps_pin",
                    "value": "PushButton,PIN"
                },
                {
                    "type": "steering_interf",
                    "value": {
                        "cur_ch": 42,
                        "rec_ch": 132
                    },
                    "subtree": "radio",
                    "index": 5
                },
                {
                    "subtree": "ssid",
                    "index": "5",
                    "type": "clients_steering_coverage",
                    "value": {
                        "cur_band": "5",
                        "rec_band": "2",
                        "macs": {
                            "00-00-00-00-00-03": -80
                        }
                    }
                }
            ],
            "total": 5,
            "detail": {
                "security_encryption": 1,
                "security_mode": 1,
                "security_wps_pin": 1,
                "steering_interf": 1,
                "clients_steering_coverage": 1
            },
            "ts": 1673515744.4641435
        },
        "pme": {},
        "changes": {
            "auto": 0,
            "axwifi": 0,
            "manual": 0,
            "owner": "auto",
            "ts": 1672483922,
            "auto_last24h": 0,
            "manual_last24h": 0,
            "axwifi_last24h": 0
        },
        "ssid": {
            "5": {
                "clients": {
                    "all": [
                        {
                            "SignalStrength": -80,
                            "OperatingStandard": "n.a.",
                            "LastDataDownlinkRate": 0,
                            "LastDataUplinkRate": 0,
                            "MACAddress": "00-00-00-00-00-03",
                            "AuthenticationState": 1,
                            "vendor": "Officially Xerox",
                            "Active": 1,
                            "ipaddress": "n.a.",
                            "AssociationTime": "n.a.",
                            "Noise": 0,
                            "snr": 0,
                            "HostName": "n.a.",
                            "Retransmissions": 0,
                            "Stats": {
                                "BytesSent": 0,
                                "BytesReceived": 0,
                                "PacketsSent": 0,
                                "PacketsReceived": 0,
                                "ErrorsSent": 0,
                                "ErrorsReceived": 0,
                                "RetransCount": 0
                            }
                        },
                        {
                            "SignalStrength": -50,
                            "OperatingStandard": "n.a.",
                            "LastDataDownlinkRate": 0,
                            "LastDataUplinkRate": 0,
                            "MACAddress": "00-00-00-00-00-02",
                            "AuthenticationState": 1,
                            "vendor": "Officially Xerox",
                            "Active": 1,
                            "ipaddress": "n.a.",
                            "AssociationTime": "n.a.",
                            "Noise": 0,
                            "snr": 0,
                            "HostName": "n.a.",
                            "Retransmissions": 0,
                            "Stats": {
                                "BytesSent": 0,
                                "BytesReceived": 0,
                                "PacketsSent": 0,
                                "PacketsReceived": 0,
                                "ErrorsSent": 0,
                                "ErrorsReceived": 0,
                                "RetransCount": 0
                            }
                        }
                    ],
                    "total": 2,
                    "good_rssi_macs": [
                        "00-00-00-00-00-02"
                    ],
                    "good_rssi": 1,
                    "low_rssi_macs": [
                        "00-00-00-00-00-03"
                    ],
                    "low_rssi": 1,
                    "i1_rssi_macs": [],
                    "i1_rssi": 0,
                    "i2_rssi_macs": [
                        "00-00-00-00-00-02"
                    ],
                    "i2_rssi": 1,
                    "i3_rssi_macs": [],
                    "i3_rssi": 0,
                    "i4_rssi_macs": [
                        "00-00-00-00-00-03"
                    ],
                    "i4_rssi": 1,
                    "i5_rssi_macs": [],
                    "i5_rssi": 0,
                    "sig_avg": -65,
                    "intervals": {
                        "i1": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i2": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i3": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i4": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i5": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        }
                    },
                    "global": {
                        "lddr": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "ldur": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "esent": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "erec": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        }
                    },
                    "good": {
                        "lddr": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "ldur": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "esent": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "erec": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        }
                    },
                    "low_rssi_macs_last24h": []
                }
            },
            "6": {
                "clients": {
                    "all": [],
                    "total": 0,
                    "good_rssi_macs": [],
                    "good_rssi": 0,
                    "low_rssi_macs": [],
                    "low_rssi": 0,
                    "i1_rssi_macs": [],
                    "i1_rssi": 0,
                    "i2_rssi_macs": [],
                    "i2_rssi": 0,
                    "i3_rssi_macs": [],
                    "i3_rssi": 0,
                    "i4_rssi_macs": [],
                    "i4_rssi": 0,
                    "i5_rssi_macs": [],
                    "i5_rssi": 0,
                    "sig_avg": 0,
                    "intervals": {
                        "i1": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i2": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i3": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i4": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        },
                        "i5": {
                            "lddr": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "ldur": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "esent": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            },
                            "erec": {
                                "all": [],
                                "max": 0,
                                "min": 0,
                                "mean": 0,
                                "median": 0,
                                "stdev": 0
                            }
                        }
                    },
                    "global": {
                        "lddr": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "ldur": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "esent": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "erec": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        }
                    },
                    "good": {
                        "lddr": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "ldur": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "esent": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        },
                        "erec": {
                            "all": [],
                            "max": 0,
                            "min": 0,
                            "mean": 0,
                            "median": 0,
                            "stdev": 0
                        }
                    }
                }
            }
        },
        "issues": {},
        "Radio": {
            "Status": "Up",
            "Enable": 1,
            "OperatingFrequencyBand": "5GHz",
            "OperatingStandards": "a,n,ac",
            "RegulatoryDomain": "DE",
            "AutoChannelEnable": 1,
            "OperatingChannelBandwidth": "80MHz",
            "PossibleChannels": "36,40,44,48,52,56,60,64,100,104,108,112,116,132,136,140",
            "Channel": 36,
            "TransmitPower": -1,
            "possible_channels": [
                36,
                40,
                44,
                48,
                52,
                56,
                60,
                64,
                100,
                104,
                108,
                112,
                116,
                132,
                136,
                140
            ],
            "noise": 0,
            "enabled": true,
            "band": "5",
            "radio_chan": 36,
            "bandwidth": 80,
            "op_standard": 6,
            "Stats": {
                "BytesSent": 36,
                "BytesReceived": 134,
                "PacketsSent": 192,
                "PacketsReceived": 276,
                "ErrorsSent": 543,
                "ErrorsReceived": 13
            }
        },
        "SSID": {
            "5": {
                "LowerLayers": "Device.WiFi.Radio.5",
                "BSSID": "54-83-3A-3B-2E-02",
                "SSID": "Zyxel_2E01_5G",
                "Stats": {
                    "BytesReceived": 11,
                    "ErrorsSent": 0,
                    "PacketsReceived": 88,
                    "ErrorsReceived": 1,
                    "BytesSent": 12,
                    "PacketsSent": 96
                },
                "Security": {
                    "ModeEnabled": "WEP-128",
                    "EncryptionMode": "TKIPEncryption"
                },
                "WPS": {
                    "Enable": 1,
                    "ConfigMethodsEnabled": "PushButton,PIN"
                },
                "SSIDAdvertisementEnabled": 1,
                "SSIDReference": "Device.WiFi.SSID.5",
                "AssociatedDevice": {
                    "1": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-02",
                        "SignalStrength": -50,
                        "AuthenticationState": 1,
                        "Type": "Client"
                    },
                    "2": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-03",
                        "SignalStrength": -80,
                        "AuthenticationState": 1,
                        "Type": "Client"
                    }
                },
                "band": "5",
                "rid": "54833A-S190Y20057813"
            },
            "6": {
                "LowerLayers": "Device.WiFi.Radio.5",
                "BSSID": "54-83-3A-3B-2E-02",
                "SSID": "Zyxel_2E01_5G_5",
                "Stats": {
                    "BytesReceived": 123,
                    "ErrorsSent": 543,
                    "PacketsReceived": 188,
                    "ErrorsReceived": 12,
                    "BytesSent": 24,
                    "PacketsSent": 96
                },
                "band": "5",
                "rid": "54833A-S190Y20057813"
            }
        },
        "scan_dt": 3887
    },
    "collector": {
        "msg": "Full Scan",
        "full_scan": 1,
        "code": 200,
        "details": "",
        "light_scan": 0,
        "light_scan_last24h": 0,
        "full_scan_last24h": 0
    },
    "cpe": {
        "recommendations": {
            "all": [
                {
                    "type": "mem_usage",
                    "value": 99.9,
                    "threshold": 90
                }
            ],
            "total": 1,
            "detail": {
                "mem_usage": 1
            },
            "ts": 1673515744.4641435
        }
    },
    "id": "54833A-S190Y20057813",
    "ts": 1673515744.348,
    "conf": {
        "country": "Europe",
        "upper_chan_2": 13
    },
    "metadata": {
        "allow_auto_enforce_5": null,
        "cid": "foo",
        "last_scan_ts": 1593765588366,
        "allow_collection": 1,
        "allow_auto_enforce_2": 1,
        "tenant_id": "Y3J5cHRvaGFzaA=="
    },
    "nr": 1,
    "WiFi": {
        "NeighboringWiFiDiagnostic": {
            "scan_dt": 6009,
            "coll_dt": 3887,
            "DiagnosticsState": "Complete",
            "ResultNumberOfEntries": 56
        },
        "Radio": {
            "1": {
                "Status": "Up",
                "Enable": 1,
                "OperatingChannelBandwidth": "20MHz",
                "OperatingFrequencyBand": "2.4GHz",
                "OperatingStandards": "n",
                "RegulatoryDomain": "DE",
                "AutoChannelEnable": 0,
                "PossibleChannels": "1,2,3,4,5,6,7,8,9,10,11,12,13",
                "Channel": 11,
                "TransmitPower": -1,
                "possible_channels": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13
                ],
                "noise": 0,
                "enabled": true,
                "band": "2",
                "radio_chan": 11,
                "bandwidth": 20,
                "op_standard": 4,
                "Stats": {
                    "BytesSent": 24,
                    "BytesReceived": 22,
                    "PacketsSent": 192,
                    "PacketsReceived": 176,
                    "ErrorsSent": 0,
                    "ErrorsReceived": 2,
                    "BytesReceivedPerSec": -28.683196603509927,
                    "BytesSentPerSec": -0.0005390399969887958
                },
                "upper_channel": 13
            },
            "5": {
                "Status": "Up",
                "Enable": 1,
                "OperatingFrequencyBand": "5GHz",
                "OperatingStandards": "a,n,ac",
                "RegulatoryDomain": "DE",
                "AutoChannelEnable": 1,
                "OperatingChannelBandwidth": "80MHz",
                "PossibleChannels": "36,40,44,48,52,56,60,64,100,104,108,112,116,132,136,140",
                "Channel": 36,
                "TransmitPower": -1,
                "possible_channels": [
                    36,
                    40,
                    44,
                    48,
                    52,
                    56,
                    60,
                    64,
                    100,
                    104,
                    108,
                    112,
                    116,
                    132,
                    136,
                    140
                ],
                "noise": 0,
                "enabled": true,
                "band": "5",
                "radio_chan": 36,
                "bandwidth": 80,
                "op_standard": 6,
                "Stats": {
                    "BytesSent": 36,
                    "BytesReceived": 134,
                    "PacketsSent": 192,
                    "PacketsReceived": 276,
                    "ErrorsSent": 543,
                    "ErrorsReceived": 13,
                    "BytesReceivedPerSec": 0.00012991251725988964,
                    "BytesSentPerSec": 3.490187030862707e-05
                }
            }
        },
        "SSID": {
            "1": {
                "BSSID": "54-83-3A-3B-2E-01",
                "LowerLayers": "Device.WiFi.Radio.1",
                "SSID": "Zyxel_2E01",
                "Stats": {
                    "BytesReceived": 11,
                    "ErrorsSent": 0,
                    "PacketsReceived": 88,
                    "ErrorsReceived": 1,
                    "BytesSent": 12,
                    "PacketsSent": 96,
                    "ErrorsReceivedPerSec": 9.69496397461863e-07,
                    "ErrorsSentPerSec": 0,
                    "PacketsReceivedPerSec": -0.14626598249227635,
                    "PacketsSentPerSec": 8.919366856649139e-05,
                    "BytesReceivedPerSec": -28.6832072679703,
                    "BytesSentPerSec": -0.0005506739537583382
                },
                "Security": {
                    "ModeEnabled": "WEP-128",
                    "EncryptionMode": "None"
                },
                "SSIDAdvertisementEnabled": 1,
                "SSIDReference": "Device.WiFi.SSID.1",
                "AssociatedDevice": {
                    "1": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-00",
                        "SignalStrength": -50,
                        "AuthenticationState": 1,
                        "Type": "Client"
                    },
                    "2": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-01",
                        "SignalStrength": -80,
                        "AuthenticationState": 1,
                        "OperatingStandard": "b",
                        "Type": "Client"
                    }
                },
                "band": "2",
                "rid": "54833A-S190Y20057813"
            },
            "2": {
                "BSSID": "54-83-3A-3B-2E-01",
                "LowerLayers": "Device.WiFi.Radio.1",
                "SSID": "Zyxel_2E01_G",
                "Stats": {
                    "BytesReceived": 11,
                    "ErrorsSent": 0,
                    "PacketsReceived": 88,
                    "ErrorsReceived": 1,
                    "BytesSent": 12,
                    "PacketsSent": 96,
                    "ErrorsReceivedPerSec": 9.69496397461863e-07,
                    "ErrorsSentPerSec": 0,
                    "PacketsReceivedPerSec": 8.531568297664394e-05,
                    "PacketsSentPerSec": 9.307165415633884e-05,
                    "BytesReceivedPerSec": 1.0664460372080493e-05,
                    "BytesSentPerSec": 1.1633956769542355e-05
                },
                "band": "2",
                "rid": "54833A-S190Y20057813"
            },
            "5": {
                "LowerLayers": "Device.WiFi.Radio.5",
                "BSSID": "54-83-3A-3B-2E-02",
                "SSID": "Zyxel_2E01_5G",
                "Stats": {
                    "BytesReceived": 11,
                    "ErrorsSent": 0,
                    "PacketsReceived": 88,
                    "ErrorsReceived": 1,
                    "BytesSent": 12,
                    "PacketsSent": 96,
                    "ErrorsReceivedPerSec": 9.69496397461863e-07,
                    "ErrorsSentPerSec": 0,
                    "PacketsReceivedPerSec": 8.531568297664394e-05,
                    "PacketsSentPerSec": 9.307165415633884e-05,
                    "BytesReceivedPerSec": 1.0664460372080493e-05,
                    "BytesSentPerSec": 1.1633956769542355e-05
                },
                "Security": {
                    "ModeEnabled": "WEP-128",
                    "EncryptionMode": "TKIPEncryption"
                },
                "WPS": {
                    "Enable": 1,
                    "ConfigMethodsEnabled": "PushButton,PIN"
                },
                "SSIDAdvertisementEnabled": 1,
                "SSIDReference": "Device.WiFi.SSID.5",
                "AssociatedDevice": {
                    "1": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-02",
                        "SignalStrength": -50,
                        "AuthenticationState": 1,
                        "Type": "Client"
                    },
                    "2": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-03",
                        "SignalStrength": -80,
                        "AuthenticationState": 1,
                        "Type": "Client"
                    }
                },
                "band": "5",
                "rid": "54833A-S190Y20057813"
            },
            "6": {
                "LowerLayers": "Device.WiFi.Radio.5",
                "BSSID": "54-83-3A-3B-2E-02",
                "SSID": "Zyxel_2E01_5G_5",
                "Stats": {
                    "BytesReceived": 123,
                    "ErrorsSent": 543,
                    "PacketsReceived": 188,
                    "ErrorsReceived": 12,
                    "BytesSent": 24,
                    "PacketsSent": 96,
                    "ErrorsReceivedPerSec": 1.1633956769542355e-05,
                    "ErrorsSentPerSec": 0.0005264365438217917,
                    "PacketsReceivedPerSec": 0.00018226532272283023,
                    "PacketsSentPerSec": 9.307165415633884e-05,
                    "BytesReceivedPerSec": 0.00011924805688780915,
                    "BytesSentPerSec": 2.326791353908471e-05
                },
                "band": "5",
                "rid": "54833A-S190Y20057813"
            }
        },
        "AccessPoint": {
            "1": {
                "Security": {
                    "ModeEnabled": "WEP-128",
                    "EncryptionMode": "None"
                },
                "SSIDAdvertisementEnabled": 1,
                "SSIDReference": "Device.WiFi.SSID.1",
                "AssociatedDevice": {
                    "1": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-00",
                        "SignalStrength": -50,
                        "AuthenticationState": 1,
                        "Type": "Client"
                    },
                    "2": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-01",
                        "SignalStrength": -80,
                        "AuthenticationState": 1,
                        "OperatingStandard": "b",
                        "Type": "Client"
                    }
                }
            },
            "5": {
                "Security": {
                    "ModeEnabled": "WEP-128",
                    "EncryptionMode": "TKIPEncryption"
                },
                "WPS": {
                    "Enable": 1,
                    "ConfigMethodsEnabled": "PushButton,PIN"
                },
                "SSIDAdvertisementEnabled": 1,
                "SSIDReference": "Device.WiFi.SSID.5",
                "AssociatedDevice": {
                    "1": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-02",
                        "SignalStrength": -50,
                        "AuthenticationState": 1,
                        "Type": "Client"
                    },
                    "2": {
                        "Active": 1,
                        "MACAddress": "00-00-00-00-00-03",
                        "SignalStrength": -80,
                        "AuthenticationState": 1,
                        "Type": "Client"
                    }
                }
            }
        },
        "RadioRefs": {
            "2": "1",
            "5": "5"
        }
    },
    "DeviceInfo": {
        "MemoryStatus": {
            "Total": 10000,
            "Free": 10,
            "usage": 99.9
        },
        "ProcessStatus": {
            "CPUUsage": 90
        },
        "UpTime": 73920,
        "HardwareVersion": "EMG3525-T50B",
        "ModelName": "EMG3525-T50B",
        "SerialNumber": "S190Y20057813",
        "SoftwareVersion": "V5.50(ABPM.0)D0",
        "ManufacturerOUI": "54833A",
        "ProductClass": "EMG3525-T50B",
        "Manufacturer": "Zyxel"
    },
    "score": 57
}
