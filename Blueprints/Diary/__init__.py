from sqlite3 import Error
from Utilities.Db_utilities import table_ids
from flask import Blueprint
from flask_login import current_user, login_required



def create_diary_entries_table(i, conn):
    try:
        sql_create_users_table = """ CREATE TABLE IF NOT EXISTS diary (
                                        entry_id TEXT PRIMARY KEY,  
                                        date TEXT,
                                        entry TEXT
                                    ); """
        if conn is not None:
            conn.execute(sql_create_users_table)
        else:
            print("Error! could not create diary table")
    except Error as e:
        print(e)
    conn.execute('INSERT OR IGNORE INTO tables(table_index, table_name) VALUES (?,?)', (i, 'tasks'))
    conn.commit()
    table_ids.diary=i

diary = Blueprint('Diary', __name__)
from . import routes

@diary.before_request
def require_login():
    if not current_user.is_authenticated:
        return login_required()