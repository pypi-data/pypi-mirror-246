"""
Produces a local mysql server with
bin/mysqld start script
bin/mysql  client script connecting as root
"""


from devapp.tools import read_file, write_file, exists, offset_port, project
from devapp.tools import wait_for_port
from devapp.app import app, do, system
import os, time

T = '''
[server]
[mysqld]
datadir=%(d_data)s
socket=%(d_tmp)s/mysql.sock
log-error=%(fn_err_log)s
pid-file=%(fn_pid)s
port=%(port)s

[galera]
# Mandatory settings
#wsrep_on=ON
#wsrep_provider=
#wsrep_cluster_address=
#binlog_format=row
#default_storage_engine=InnoDB
#innodb_autoinc_lock_mode=2
#
# Allow server to accept connections on all interfaces.
#
#bind-address=0.0.0.0
port=%(port)s
#
# Optional setting
#wsrep_slave_threads=1
#innodb_flush_log_at_trx_commit=0

# this is only for embedded server
[embedded]

# This group is only read by MariaDB servers, not by MySQL.
# If you use the same .cnf file for MySQL and MariaDB,
# you can put MariaDB-only options here
[mariadb]
'''
from time import sleep
from uuid import uuid4
from functools import partial

# this is for initializing time only:
env_root_pw_key = 'password_mysql_root'
init_pw = os.environ.get(env_root_pw_key) or str(uuid4())
fn_dflt = lambda: '--defaults-file="%s/conf/mysql/my.cnf"' % project.root()


def dirs():
    r = project.root()
    m = {'d_' + k: r + '/%s/mysql' % k for k in ['data', 'log', 'tmp', 'conf']}
    return m


def client(exe, port, pw):
    s = '%s -uroot --port=%s --host=127.0.0.1 "-p%s"'
    return s % (exe, port, pw)


class mysql:
    def mysql(**kw):
        port = offset_port(3306)
        cmd = client('mysql', port, '${%s:-}' % env_root_pw_key)
        return {
            'env': {env_root_pw_key: init_pw},
            'cmd': cmd,
        }

    def mysqld(**kw):
        return 'mysqld ' + fn_dflt()

    def post_install(rsc, install=False, verify=False, **kw):
        """Creates the initial DB after conda install plus sets up root pw
        and mysql client.
        """
        port = offset_port(3306)
        ctx = dirs()
        if verify:
            d = ctx['d_data']
            return exists(d) and bool(os.listdir(d))

        w = wait_for_port(port, '127.0.0.1', timeout=0.1, log_err=False)
        if w:
            app.die('mysql port occupied - cannot init mysql', port=port)

        for k, v in ctx.items():
            os.makedirs(v, exist_ok=True)

        ctx['fn_pid'] = '%(d_tmp)s/mysql.pid' % ctx
        ctx['fn_conf'] = '%(d_conf)s/my.cnf' % ctx
        ctx['fn_err_log'] = '%(d_log)s/err.log' % ctx
        ctx['port'] = port
        write_file(ctx['fn_conf'], T % ctx)
        mysql = kw['api'].rsc_path(rsc) + '/mysql'
        mysqld = mysql + 'd ' + fn_dflt()
        cmd = mysqld + ' --initialize'
        app.warn('Initializing mysql...', cmd=cmd)
        system(cmd)
        # get autocreated one time pw from log - we have to change it:
        cmd = 'tail -n 200 "%(fn_err_log)s" | grep "password" | tail -n 1' % ctx
        pw = os.popen(cmd).read().split()[-1].strip()
        mysql = client(mysql + ' --connect-expired-password', port, pw)
        try:
            app.info('first start mysqld')
            system(mysqld + '&')
            if not wait_for_port(port, '127.0.0.1'):
                app.die('mysql did not start', port=port)
            app.info('port is up', port=port)
            cmd = "ALTER USER 'root'@'localhost' IDENTIFIED BY '%s';" % init_pw
            cmd = mysql + ' --user=root -e "%s"' % cmd
            err = 0
            for tries in range(10):
                time.sleep(0.1)
                err = system(cmd)
                if not err:
                    break
            if err:
                app.die('Could not connect to first started mysqld')
        finally:
            pid = int(read_file(ctx['fn_pid']).strip())
            os.kill(pid, 15)
            app.info('stopped server')
            app.info('mysql initialized')
