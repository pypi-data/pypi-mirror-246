import os
import time
from devapp.app import app
from devapp.tools import get_deep, deep_update, tn, read_file, project, offset_port
from rx import create
import ujson as json
from functools import partial
from datetime import datetime
from operators.ops.tools import Rx, rx, rx_operator
from tree_builder import links
from operators.ops.tools import rx_operator

try:
    from sqlalchemy import create_engine
except Exception as ex:
    create_engine = None

env = os.environ

dflt_con_url = lambda: 'mysql+pymysql://root@127.0.0.1:%s' % offset_port(3306)
con_urls = {}
attrs = lambda cls: [i for i in dir(cls) if not i.startswith('_')]

# mysql+pymysql://root:@localhost:3306/mysql_db


g = getattr


def exec_sql(eng, sql, data=None, on_read=None):
    app.debug(sql, **data) if data else app.debug(sql)
    if isinstance(eng, str):
        eng = con_urls[eng]['engine']
    if not data:
        res = eng.execute(sql)
    else:
        res = eng.execute(sql, data)
    if on_read:
        for r in res:
            # pushing
            on_read(r)
        return
    # return iterator:
    return res


def get_mysql_password(parsed_url, proj_root):
    m = parsed_url
    pw = m['password'] = m.get('password', env.get('password_mysql_root'))
    if pw == None:
        # . is sh AND bash, source is not:
        cmd = '. %s/bin/mysql && echo $password_mysql_root' % proj_root
        pw = os.popen(cmd).read().strip()
    return pw


def get_engine(url):
    root = project.root()
    con = con_urls.get(url)
    if con:
        return con['engine']
    if not '://' in url:
        fn = root + '/conf/mysql/urls.json'
        urls = read_file(fn, dflt='')
        if not urls:
            app.die('Cannot read conn url name, missing file', fn=fn, name=url)
        try:
            urls = json.loads(urls)
        except Exception:
            app.die('Cannot parse', fn=fn, name=url)
        url = urls.get(url)
        if not url:
            app.die('mysql url not defined', fn=fn, name=url, have=urls.keys())
    m = links.parse_via(url)
    m['password'] = get_mysql_password(m, root)
    eng = get_engine_by_spec(m)
    con_urls[url] = {'spec': m, 'engine': eng}
    return eng


def get_engine_by_spec(spec, autocreate_db=True):
    """Autocreates the database when not present"""
    spec['path'] = path = spec.get('path', '/')
    url = '%(scheme)s://%(username)s:%(password)s@%(hostname)s:%(port)s%(path)s' % spec
    err_msg = 'cannot connect to database server'
    try:
        engine = create_engine(url)
        engine.connect()
        return engine
    except Exception as ex:
        if path == '/' or not autocreate_db:
            app.error(err_msg, exc=ex, **spec)
            raise Exception(err_msg)
        path = spec.pop('path')
        try:
            e = get_engine_by_spec(spec, autocreate_db=False)
            db = path[1:]  # /db
            app.warn('Creating database', db=db)
            exec_sql(e, 'create database %s' % db)
            spec['path'] = path
        except Exception as ex:
            app.error('cannot connect to database server', exc=ex, **spec)
            raise Exception(err_msg)
        return get_engine_by_spec(spec, autocreate_db=False)


def connect(SQL):
    """
    - Scans a SQL setup root class
    - connects to all dbs
    - creates tables
    - remembers all con_urls in global con_urls dict

    Setup like

    class SQL:
        con_url = <dflt_con_url>
        class db1:
            [con_url = <optional other connection url>] # default: global one
            [user = ..] # restricted to this db - for clients
            [password = ..] # env vars resolved
            class Tables:
                tbl1 = '<Create statement for tbl1>'
            class prepared_stmt_1:
                [con_url = <optional other connection url>] # default: that of db1
                [id = 'id']# default 
                sql = '<Prepared statement>'
                [fields = id, username] # only for read ops required, those will be put into data
            (...)

    - All optionals will be setattr-ed at connect time
    - All dbs created
    - All tables created
    - All class type attrs of DBs are considered prepared_stmts

    # Restrictions:
    - Currently only single primary key reads (todo: support tuple ids)
    - Only top level data ops (todo: support access keys like with redis and/or result handlers)
    - No reconnects on error (do in exec_sql) 
    - Immediate connect tries on client connect to hub (in setup)

    All straight forward in the stmt classes.
    
    """
    if g(SQL, '_set_up', None):
        return
    g_url = g(SQL, 'con_url', dflt_con_url())
    for db in attrs(SQL):
        DB = g(SQL, db)
        if not isinstance(DB, type):
            continue
        app.info('Connecting to database', db=db)
        url = g(DB, 'con_url', g_url)
        if not url.endswith(db):
            url += '/' + db
        eng = get_engine(url)
        DB.con_url = url
        have = [i[0] for i in exec_sql(eng, 'show tables')]
        for t in attrs(DB.Tables):
            if not t in have:
                v = g(DB.Tables, t)
                app.warn('Creating table', table=t)
                exec_sql(eng, v)
        add_user(eng, DB, g(DB, 'user', None))
        for key in attrs(DB):
            if key == 'Tables':
                continue
            stmt = g(DB, key)
            if not isinstance(stmt, type):
                continue
            if not hasattr(stmt, 'id'):
                stmt.id = 'id'  # default
            if hasattr(stmt, 'sql'):
                stmt.con_url = g(stmt, 'con_url', DB.con_url)
                get_engine(url)
    app.info('Have connections', json=list(con_urls.keys()))

    SQL._set_up = True


def add_user(eng, DB, username):
    if not username:
        return
    db = DB.__name__
    password = g(DB, 'password', 0)
    if not password:
        app.die('No password for user given', user=username, db=db)
    host = g(DB, 'host', '%%')
    user = dict(locals())
    udel = "DROP USER '%(username)s'@'%(host)s'"
    ucrea = "CREATE USER IF NOT EXISTS '%(username)s'@'%(host)s' IDENTIFIED BY '%(password)s'"
    ugrant = "GRANT ALL ON `%(db)s`.* TO '%(username)s'@'%(host)s'"
    # drop would fail w/o it:
    for sql in ucrea, udel, ucrea, ugrant:
        exec_sql(eng, sql % user)
    app.info('Created client account', user=username, db=db, host=host)


from operators.con.connections import con_params


class mysql:
    class con_defaults:
        setup = None

    @classmethod
    def _connect(cls):
        d = con_params(cls)
        connect(d['setup'])

    @classmethod
    def do_sql(cls, stmt, db, func):
        spec = [0]
        if db is None:
            db, stmt = stmt.split('.')

        def setup(db=db, stmt=stmt, spec=spec):
            SQL = con_params(cls)['setup']
            connect(SQL)
            # After connect (parsing the SQL setup) we have all we need in the statement
            # classes:
            spec[0] = g(g(SQL, db), stmt)

        def disconnect(spec=spec):
            breakpoint()  # FIXME BREAKPOINT

        func = partial(func, spec=spec)

        return rx_operator(on_subscription=setup, on_next=func, on_completed=disconnect)

    @classmethod
    def _exec_sql(cls, *a, **kw):
        return exec_sql(*a, **kw)

    @classmethod
    def read(cls, stmt, db=None, is_rx=True):
        def read(data, msg, spec):
            spec = spec[0]
            res = cls._exec_sql(spec.con_url, spec.sql, data)
            for u in res:
                break
            i = 0
            for f in spec.fields:
                data[f] = u[i]
                i += 1

        return cls.do_sql(stmt, db, read)

    @classmethod
    def write(cls, stmt, db=None, is_rx=True):
        def write(data, msg, spec):
            spec = spec[0]
            res = cls._exec_sql(spec.con_url, spec.sql, data)
            data[spec.id] = res.lastrowid

        return cls.do_sql(stmt, db, write)
