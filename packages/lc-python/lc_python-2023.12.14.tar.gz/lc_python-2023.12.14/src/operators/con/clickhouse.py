from datetime import datetime

from devapp.app import app
from operators.con import con_params
from operators.ops.tools import rx_operator
from operators.misc_util import getter

import clickhouse_connect


def perc(f):
    return int((f * 100) + 0.5)


def byte(i):
    return i


def autoch(s):
    return True if str(s).lower() in ('1', 'true', 'on') else False


def to_date_time(ts):
    return datetime.utcfromtimestamp(ts)


def short(i):
    return int(i)


def long(i):
    return int(i)


def geo_point(md):
    return [md.get('longitude', 0), md.get('latitude', 0)]


g = getattr
types = {
    byte: 'UInt8',
    short: 'Int16',
    long: 'Int64',
    int: 'Int32',
    perc: 'UInt8',
    bool: 'Bool',
    str: 'String',
    # 'order_date'      : partial(ES.Date,format='epoch_millis'),
    to_date_time: 'DateTime',
    # 'cid'             : text_kw,
    # 'disp_stream_id'  : text_kw,
    # 'disp_proc_id'    : text_kw,
    # 'disp_data_id'    : text_kw,
    geo_point: 'Point',
}

is_ = isinstance
str_types = dict([(k.__name__, k) for k in types if not is_(k, str)])

rec_ch = 'recommended_channel'


def make_mapping(Def):
    """
    This replaces the attribute definition tuples of a Def class with real
    value getters, so items get be produced later.
    Also it returns an table field names mapped to their types to be used
    in table creation.
    """

    table_structure = {}
    Def._keys = [k for k in dir(Def) if not k.startswith('_')]
    for k in Def._keys:
        v = g(Def, k)
        if isinstance(v, str):
            v += ':str'
            v = [v]
        if len(v) == 1:
            v = v[0]
            v, typ = v.split(':')[:2]
            typ = str_types.get(typ, typ)
            default = None
            is_index = False
        elif len(v) == 2:
            v, typ, default, is_index = v[0], v[1], None, False
        elif len(v) == 3:
            v, typ, default, is_index = v[0], v[1], v[2], False
        else:
            v, typ, default, is_index = v
        setattr(Def, k, getter(v, typ, default))
        field_typ = types.get(k) or types[typ]
        table_structure[k] = (field_typ, is_index)

    return table_structure


class clickhouse:
    name = 'clickhouse'
    url = ''

    class con_defaults:
        port = 8123
        host = 'localhost'
        db_name = 'axwifi'
        table_name = 'axwifi'
        username = 'default'
        password = ''

    @classmethod
    def _make_table_if_not_there(cls, con):
        client = con['client']
        res = client.command(f"SHOW TABLES LIKE '{con['table_name']}'")
        if res == con['table_name']:
            app.info(
                f"The table {con['table_name']} already exists in clickhouse, continueing"
            )
        else:
            try:
                table_creation_command = f"""CREATE TABLE {con['table_name']}  
                                  (key String) 
                                  ENGINE MergeTree ORDER BY key
                                  """
                res = con['client'].command(table_creation_command)
            except Exception as exc:
                app.error(f"Can not create table {con['table_name']}, {exc}")
                return False
            app.info(f"Created table {con['table_name']} for clickhouse")
        return True

    @classmethod
    def _ensure_all_fields_in_table(cls, con, table_structure):
        client = con['client']
        table_name = con['table_name']
        # find all indexes
        db_indexes = []
        res = client.query(f'SHOW INDEX FROM {table_name}')
        for _table, _non_unique, key_name, _seq_in_index, _column_name, *_ in res.result_rows:
            db_indexes.append(key_name) # we define indexes as id(id)
        res = client.query(f"DESCRIBE TABLE '{table_name}'")
        for f_name, f_type, *_ in res.result_rows: # remove the already present ones from table structure
            table_structure_type, table_structure_is_index = table_structure.get(f_name, (None, None))
            if table_structure_type == f_type:
                table_structure.pop(f_name)
                if table_structure_is_index and f_name not in db_indexes:
                    try:
                        app.info(f'Adding index {f_name} on table {table_name}')
                        client.command(f'ALTER TABLE {table_name} ADD INDEX {f_name}({f_name}) TYPE minmax')
                    except Exception as exc:
                        app.error(f'Error adding index {f_name} on table {table_name}, {exc}')

        for f_name, (f_type, is_index) in table_structure.items():
            # create the ones which were not already in the table
            try:
                app.info(f'Adding {f_name} column to clickhouse table {table_name}')
                client.command(f'ALTER TABLE {table_name} ADD COLUMN {f_name} {f_type};')
            except Exception as exc:
                app.error(f'Error adding column, Exception: {exc}')
            if is_index and f_name not in db_indexes:
                try:
                    app.info(f'Adding index {f_name} on table {table_name}')
                    client.command(f'ALTER TABLE {table_name} ADD INDEX {f_name}({f_name}) TYPE minmax')
                except Exception as exc:
                    app.error(f'Error adding index {f_name} on table {table_name}, {exc}')

    @classmethod
    def snk(cls, is_rx=True, **cfg):
        app.info('Clickhouse snk initializing')
        con = con_params(cls, defaults=cls.con_defaults)
        con.update(cfg)

        cls.attrs = getattr(cls, 'con_attributes', None)
        cls.table_structure = make_mapping(cls.attrs)
        cls.rg_getters = [(k, g(cls.attrs, k)) for k in cls.attrs._keys]

        def open_connection(con=con):
            try:
                con['client'] = clickhouse_connect.get_client(
                    host=con['host'], username=con['username'], password=con['password']
                )
                cls._make_table_if_not_there(con)
                cls._ensure_all_fields_in_table(con, cls.table_structure)
            except Exception as exc:
                app.error(f'Error connecting to clickhouse using {con}, {exc}')

        def write(
            data,
            msg,
            con=con,
            attrs=cls.attrs,
            table_structure=cls.table_structure,
            getters=cls.rg_getters,
        ):
            app.debug('Writing to clickhouse')
            table_name = con['table_name']
            client = con['client']
            values = []
            column_names = []
            for k, g in getters:
                v = g(data)
                if v is not None:
                    column_names.append(k)
                    values.append(g(data))
            try:
                client.insert(table_name, [values], column_names=column_names)
            except Exception as exc:
                app.error(f'could not write to Clickhouse table {table_name}; {exc}')

        def close_connection(con=con):
            try:
                con['client'].disconnect_connection()
            except Exception as exc:
                app.error(f'could not close clickhouse {con["client"]}; {exc}')

        return rx_operator(
            on_subscription=open_connection, on_next=write, on_completed=close_connection
        )
