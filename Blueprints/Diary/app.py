from flask import Flask, Blueprint,  render_template, request
from backend import submit_entry, view_entries, view_date_range
from datetime import date

app=Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('diary_entry_page.html')

@app.route('/entries/<date_str>')
def view_day_entries(date_str):
    date_obj = date.fromisoformat(date_str)
    diary_day=view_entries(date_obj)
    return render_template('view_diary_page.html', dates=[diary_day])

@app.route('/date_range')
def view_date_range_page():
    start_date = date.fromisoformat(request.args.get('start_date'))
    end_date = date.fromisoformat(request.args.get('end_date'))
    entries = view_date_range(start_date, end_date)
    return render_template('view_diary_page.html', dates = entries)

@app.route('/api/submit_entry', methods = ['POST'])
def submit_entry_api():
    date_str = request.form['date']
    date_obj = date.fromisoformat(date_str)
    submit_entry(date_obj, request.form['entry'])
    return '', 204

@app.route('/api/entries/<date>', methods = ['GET'])
def get_day_entries(date_str):
    date_obj = date.fromisoformat(date_str)
    return view_entries([date_obj])
    




