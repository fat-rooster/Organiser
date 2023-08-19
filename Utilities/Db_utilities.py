from flask import g
import sqlite3
from sqlite3 import Error

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('./organiser_db.sqlite') # Creates the file if it does not exist
        conn.row_factory = dict_factory
        conn.execute('PRAGMA foreign_keys = ON')
        print(f'Successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(f'An error occurred: {e}')
    return conn

def get_db():
    if 'db' not in g:
        g.db = create_connection()
    return g.db

def link_tables():
    create_tables()


def remove_entity(entity_id):
    conn = get_db()
    sql = ''' DELETE FROM entities WHERE entity_id = ? '''
    cur = conn.cursor()
    n=cur.rowcount
    cur.execute(sql, (entity_id,))
    conn.commit()
    m=n-cur.rowcount
    if (m==0): 
        print('delete failed')
        return False
    return True

def create_tables_table(conn):
    try:
        sql_create_tables_table = """ CREATE TABLE IF NOT EXISTS tables (
                                        table_index INTEGER PRIMARY KEY,
                                        table_name TEXT
                                    ); """
        if conn is not None:
            conn.execute(sql_create_tables_table)
        else:
            print("Error! could not create tables table")
    except Error as e:
        print(e)

def create_entities_table(conn):
    try:
        sql_create_entities_table = """ CREATE TABLE IF NOT EXISTS entities (
                                        entity_id TEXT PRIMARY KEY,
                                        table_index INTEGER REFERENCES tables(table_index)
                                    ); """
        if conn is not None:
            conn.execute(sql_create_entities_table)
        else:
            print("Error! could not create entities table")
    except Error as e:
        print(e)

def create_connections_table(conn):
    try:
        sql_create_users_table = """ CREATE TABLE IF NOT EXISTS connections (
                                        source_id TEXT,
                                        dest_id TEXT,
                                        PRIMARY KEY (source_id, dest_id),
                                        FOREIGN KEY (source_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
                                        FOREIGN KEY (dest_id) REFERENCES entities(entity_id) ON DELETE CASCADE
                                    ); """
        if conn is not None:
            conn.execute(sql_create_users_table)
            conn.execute('CREATE INDEX IF NOT EXISTS idx_sources ON connections(source_id)')
        else:
            print("Error! could not create connections table")
    except Error as e:
        print(e)

class Empty:
    pass

table_ids=Empty()

def create_tables(conn):
    create_entities_table(conn)
    create_tables_table(conn)
    create_connections_table(conn)


def db_build():
    conn=create_connection()
    create_tables(conn)
    return conn

def get_user(user_id):
    conn=get_db()
    cur = conn.cursor()
    print(user_id)
    cur.execute('SELECT user_name FROM users WHERE user_id = ?', (user_id,))
    user_name = cur.fetchone()
    return user_name['user_name'] if user_name else None

def get_user_id(user_name):
    conn=get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM users WHERE user_name = ?', (user_name, ))
    user_id = cur.fetchone()
    return user_id['user_id'] if user_id else None