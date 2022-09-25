import sqlite3 as sl


def create_tables(file_db):
    str_connect = f'file:{file_db}'

    con = sl.connect(str_connect, uri=True)
    cur = con.cursor()

    cur.execute("""create table if not exists channel
(
    channel_id integer
        constraint channel_pk
            primary key,
    is_admin   bool default FALSE not null,
    is_base    bool default FALSE,
    is_test    bool default FALSE,
    is_command bool default FALSE not null
);""")
    con.commit()

    cur.execute("""create table if not exists "trigger"
(
    trigger_id    integer
        constraint trigger_pk
            primary key autoincrement,
    text_request  str not null,
    text_response str not null
);""")
    con.commit()

    cur.execute("""create table if not exists "variables"
    (
        id integer constraint variables_pk primary key autoincrement,
        variable_name str not null,
        data_value not null
    )
    """)
    con.commit()

    cur.execute("""create table if not exists warn
(
    user_id     bigint  not null,
    count_warns float not null
);
""")
    con.commit()
