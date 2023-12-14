from devapp.tools import read_file, write_file, exists, offset_port, project
from devapp.app import app, do, system
import os
from .rsc_mysql import mysql


def dis_search_guard(rsc, install=False, verify=False, api=None, **kw):
    d = api.rsc_path(rsc) or ''
    fn_cfg = d + '/../config/elasticsearch.yml'
    cfg = read_file(fn_cfg, dflt='')
    if verify:
        if not d:
            return False
        if not cfg or '\nsearchguard' in cfg:
            return False
        return True
    if install:
        app.warn('Disabling search guard (SSL off)', fn_cfg=fn_cfg)
        # we had a wrong install on doglr, commenting ALL out, not just search guard:
        write_file(fn_cfg, cfg.replace('\n', '\n# '))
        cmd = d + '/elasticsearch-plugin remove search-guard-5'
        cmd = 'export PATH="%s:$PATH"; ' % d + cmd
        do(system, cmd, no_fail=True, ll=20)


def elasticsearch(**kw):
    p1, p2 = offset_port(9200), offset_port(9300)
    return 'elasticsearch -Ehttp-port=%s -Etransport.tcp.port=%s' % (p1, p2)


def mongodb(**kw):
    d = project.root() + '/data/mongodb'
    if not exists(d):
        os.makedirs(d)
    p = offset_port(rsc.mongodb.port)
    return 'mongod --dbpath="%s" --port=%s' % (d, p)


from devapp.operations import resources as darsc


class rsc:
    # All defined but set to d(disabled) = True
    # see 4A how to enable e.g. mysql
    class graph_easy:
        conda_inst = 'conda install -y -c bioconda perl-app-cpanminus  && env PERL5LIB="" PERL_LOCAL_LIB_ROOT="" PERL_MM_OPT="" PERL_MB_OPT="" cpanm Graph::Easy::As_svg'
        exe = 'graph-easy'

    class mongodb:
        d = True
        cmd = mongodb
        exe = 'mongod'
        conda_chan = 'conda-forge'
        port = 27017
        conda_pkg = 'mongodb'
        systemd = 'mongod'

    class mysql:
        d = True
        conda_chan = 'conda-forge'
        port = 3306
        provides = [mysql.mysqld, mysql.mysql]
        pkg = 'mysql'
        post_inst = mysql.post_install
        systemd = 'mysqld'

    class elasticsearch:
        d = True
        cmd = elasticsearch
        conda_pkg = 'elasticsearch-bin'
        conda_chan = 'anaconda-platform'
        port = 9200
        port_wait_timeout = 20
        post_inst = dis_search_guard
        systemd = 'elasticsearch'
