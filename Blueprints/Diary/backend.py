from flask import g
import sqlite3
import uuid
from datetime import date, timedelta

def create_table(conn):
    sql = """CREATE TABLE IF NOT EXISTS diary (
        date TEXT,
        entry TEXT
    )

    """
    conn.execute(sql)

def dict_factory(cursor, row):
    fields=[column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}
def create_connection():
    conn=sqlite3.connect('diary_db.sqlite')
    conn.row_factory = dict_factory
    return conn
    
def get_db():
    if 'db' not in g:
        g.db = create_connection()
        create_table(g.db)
    return g.db

def submit_entry(date, entry):
    sql = """INSERT INTO diary(date, entry) VALUES (?, ?) """
    conn=get_db()
    conn.execute(sql, (date.isoformat(), entry))
    conn.commit()

class DiaryDay:
    def __init__(self, date, entries):
        self.date=date
        self.entries=entries
        

def view_entries(date):
    print(date)
    sql = """SELECT entry FROM diary WHERE date = ?"""
    conn=get_db()
    cur=conn.cursor()
    cur.execute(sql, (date.isoformat(),))
    entries=cur.fetchall()
    return DiaryDay(date, entries)

def view_date_range(start, end):
    delta = end - start
    date_range = range(delta.days + 1)
    def delta_to_date(i):
        return start + timedelta(days=i)
    dates= map( delta_to_date, date_range)
    return map(view_entries, dates)