from . import diary
from flask import render_template, request
from flask_login import current_user
from datetime import date
from .backend import view_entries, view_date_range, submit_entry

@diary.route('/', methods = ['GET'])
def index():
    return render_template('diary_entry_page.html')

@diary.route('/entries/<date_str>')
def view_day_entries(date_str):
    date_obj = date.fromisoformat(date_str)
    diary_day=view_entries(date_obj, current_user)
    return render_template('view_diary_page.html', dates=[diary_day])

@diary.route('/date_range')
def view_date_range_page():
    start_date = date.fromisoformat(request.args.get('start_date'))
    end_date = date.fromisoformat(request.args.get('end_date'))
    entries = view_date_range(start_date, end_date, current_user)
    return render_template('view_diary_page.html', dates = entries)

@diary.route('/api/submit_entry', methods = ['POST'])
def submit_entry_api():
    date_str = request.form['date']
    date_obj = date.fromisoformat(date_str)
    submit_entry(date_obj, request.form['entry'], [current_user.id])
    return '', 204

@diary.route('/api/entries/<date>', methods = ['GET'])
def get_day_entries(date_str):
    date_obj = date.fromisoformat(date_str)
    return view_entries([date_obj])
    
