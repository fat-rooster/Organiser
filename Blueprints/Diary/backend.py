import sqlite3
import uuid
from datetime import date, timedelta
from Utilities.Db_utilities import get_db, table_ids

def submit_entry(date, entry, tags):
    try:
        conn = get_db()
        entry_id = str(uuid.uuid4())
        conn.execute('BEGIN TRANSACTION')
        conn.execute('INSERT INTO entities(entity_id, table_index) VALUES (?, ?)', (entry_id, table_ids.diary))
        conn.execute('INSERT INTO diary(entry_id, date, entry) VALUES (?, ?, ?)', (entry_id, date.isoformat(), entry))    
        for tag in tags:
            conn.execute('INSERT INTO connections(source_id, dest_id) VALUES (?, ?)', (tag, entry_id))
        conn.commit()
    except:
        conn.rollback()
        raise

class DiaryDay:
    def __init__(self, date, entries):
        self.date=date
        self.entries=entries
        

def view_entries(date, user):
    print(date)
    sql = """
    SELECT entry FROM 
    diary 
    JOIN connections ON diary.entry_id = connections.dest_id
    WHERE connections.source_id = ?
    AND diary.date = ?
    """
    conn=get_db()
    cur=conn.cursor()
    cur.execute(sql, (user.id, date.isoformat()))
    entries=cur.fetchall()
    return DiaryDay(date, entries)

def view_date_range(start, end, user):
    delta = end - start
    date_range = range(delta.days + 1)
    def delta_to_date(i):
        return start + timedelta(days=i)
    dates= map( delta_to_date, date_range)
    def get_entries(date):
        return view_entries(date, user)
    return map(get_entries, dates)