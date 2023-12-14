"""
Provides
- our customized Node-RED
- a default client
"""
import os
from os import environ as env
from devapp.tools.resource import S, add_const, exists, write_file, FLG
from devapp.tools import download_file, write_file
from .rsc_node import node

T_flag_defs = """
from devapp.tools import define_flags
# overwrite/add project flags here:
class ProjectFlags(%(client_flags_base)s):
    pass
define_flags(ProjectFlags)
"""

T_funcs = '''
"""
Project Specific Functions

Note: This file won't be overwritten at ops project re-inits.
"""
%(client_import)s

%(flag_defs)s

class Functions(%(client_base)s):
    """Custom Project Functions and Config"""

'''

T_flags = """# Project flags

# 10: debug, 20: info, 30: warning
--log_level=10
"""


def prom_inst(ver, binary, rsc, post_inst, github_author='prometheus', **kw):
    """helper for prometheus stuff"""
    d = f'{S.conda_prefix}/static/{binary}'
    if rsc and not rsc.installed:
        prom = f'https://github.com/{github_author}/{binary}/releases/download/v{ver}/{binary}-{ver}.linux-amd64.tar.gz'
        os.makedirs(d, exist_ok=True)
        download_file(prom, d + '/installer', auto_extract=True)
    ds = f'{d}/{binary}-{ver}.linux-amd64'
    cmd = f'{ds}/{binary}'
    ret = {'cmd': ':' + cmd}
    post_inst(rsc=rsc, static_pth=ds, ret=ret)
    return ret


def prometheus(ver='2.37.7', rsc=None, **kw):
    def post_inst(**kw):
        pass

    return prom_inst(ver, 'prometheus', rsc, post_inst, **kw)


def node_exporter(ver='1.5.0', rsc=None, **kw):
    def post_inst(**kw):
        pass

    return prom_inst(ver, 'node_exporter', rsc, post_inst, **kw)


def kafka_exporter(ver='1.6.0', rsc=None, **kw):
    def post_inst(**kw):
        pass

    return prom_inst(
        ver, 'kafka_exporter', rsc, post_inst, github_author='danielqsj', **kw
    )


# static config for the process exporter:
proc_exp_yml = """
process_names:
  - name: "{{.Comm}}"
    cmdline:
    - '.+'
"""


def process_exporter(ver='0.7.10', rsc=None, **kw):
    def post_inst(static_pth, ret, **kw):
        write_file(static_pth + '/all.yml', proc_exp_yml)
        ret['cmd'] = ret['cmd'] + f' --config.path={static_pth}/all.yml'

    n = 'process-exporter'
    return prom_inst(ver, n, rsc, post_inst, github_author='ncabatoff', **kw)


client_cmd_pre = """
flagfile="$PROJECT_ROOT/conf/client.flags"
test -e "$PROJECT_ROOT/conf/$bin_name.flags" && flagfile="$PROJECT_ROOT/conf/$bin_name.flags"
test -e "$host_conf_dir/flags" && flagfile="$host_conf_dir/flags"

"""


class worker:
    cfg = dict(
        hub_titl='AX LC',
        client_import='from operators.core import ax_core_ops',
        client_base='ax_core_ops',
        client_funcs=T_funcs,
        client_flags_base='',
        client_flags=T_flags,
    )

    def cmd_(pth, api, typ='client', tab='!API,!System', **kw):
        hubs = os.environ.get(f'{typ}_lc_hubs')
        tab = os.environ.get(f'{typ}_lc_tabs', tab)
        if tab:
            tab = f'--lc_tabs="{tab}"'
        l = list(worker.cfg.keys())
        cfg = {k: api.constant(k, worker.cfg[k]) for k in l}
        cfg['flag_defs'] = fd = cfg['client_flags_base']
        if fd:
            cfg['flag_defs'] = T_flag_defs % cfg
        funcs_ = cfg['client_funcs'] % cfg
        flags_ = cfg['client_flags'] % cfg
        env['d_conf'] = d = pth + '/conf'

        for n, s in [['functions.py', funcs_], ['client.flags', flags_]]:
            fn = d + '/' + n
            if not exists(fn):
                write_file(fn, s)

        po = '' if not FLG.port_offset else ' --port_offset=%s' % FLG.port_offset
        name = os.environ.get(f'{typ}_name', typ)
        functions = os.environ.get(f'{typ}_functions', 'functions')
        if ':' not in functions:
            functions += ':Functions'
        cmd = f':app client --flagfile="$flagfile" -cf={functions} --lc_client_name="{name}$inst_postfix-$HOSTNAME" '
        cmd += tab + po
        if hubs:
            cmd += ' --lc_hubs="%s"' % hubs
        cmd = cmd.replace(' --', ' \\\n    --')
        return {'cmd': cmd, 'cmd_pre': client_cmd_pre}

        # cp = 'export PYTHONPATH="%(d_conf)s:%(PYTHONPATH)s"\n'
        # cp += 'export PATH="%(PATH)s"\n\n'
        # return {'cmd_pre': cp % env, 'cmd': ':app client -cf functions:Functions ' + tab}

    def client(typ='client', tab='!API,!System', **kw):
        return worker.cmd_(typ=typ, tab=tab, **kw)

    def api(typ='api', tab='API,!System', **kw):
        return worker.cmd_(typ=typ, tab=tab, **kw)

    def worker(typ='worker', tab='', **kw):
        """"""
        return worker.cmd_(typ=typ, tab=tab, **kw)


class rsc_blueprint:
    """Python Reference Implementation of AX Low Code Worker Process

    Parametrize start wrapper (created by ops install in bin dir):
    Set environ parameters, prefixed by `<name>_` to desired value.
    Example:
    `client_name=myclient  client_lc_tabs='!System'  ops p i -m client -icau`
    """

    n = 'AX LC Worker Process'
    pkg = False
    systemd = True
    environ = ['instances', 'lc_tabs', 'lc_hubs', 'name', 'functions']


class rsc:
    class client(rsc_blueprint):
        cmd = worker.client

    class api(rsc_blueprint):
        cmd = worker.api

    class worker(rsc_blueprint):
        cmd = worker.worker

    class prometheus:
        cmd = prometheus
        pkg = False
        systemd = 'prometheus'

    class node_exporter:
        cmd = node_exporter
        pkg = False
        systemd = 'node_exporter'

    class process_exporter:
        cmd = process_exporter
        pkg = False
        systemd = 'process_exporter'

    class kafka_exporter:
        cmd = kafka_exporter
        pkg = False
        systemd = 'kafka_exporter'

    class nodejs:
        """
        Env vars:
            - hub_admin_auth=myadmin:mypass:*,myuser:mypass2:read,... (or the complete adminAuth dict)
            - hub_theme=aurora
            - hub_log_level=trace
        """

        cmd = 'node'
        provides = [node.npm, node.hub, node.hubdebug]
        pkg = 'nodejs'
        post_inst = node.ax_npm_install_and_link_project
        # post_inst_req = 'rpl'
        port = 1880
        wait_port = 1881
        systemd = 'hub'
        environ = ['admin_auth', 'theme', 'log_level']  # not in use currently.

    class graphviz:
        # flow arranger
        u = 'node arranger'
        n = 'Graphviz'
        cmd = 'dot'
        pkg = 'pygraphviz'
        conda_chan = 'conda-forge'
