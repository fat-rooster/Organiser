from flask import Blueprint, render_template, redirect, url_for, request, g, jsonify, send_from_directory
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
import uuid
import requests
from usermodel import User

from backend import get_db, add_task, get_task, remove_task







# Endpoint for displaying a single task
@app.route('/', methods=['GET'])
def empty_request():
    if current_user.is_authenticated:
        return send_from_directory('static', 'task.html')
    return redirect(url_for('login_page'))



# Endpoint for submitting a new task
@app.route('/submit_task', methods=['GET'])
@login_required
def submit_task():
    return send_from_directory('static', 'submit_task.html')

@app.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('empty_request'))


@app.route('/all_tasks', methods = ['GET'])
def get_all_tasks():
    response = requests.get('http://localhost:5000/api/get_all')
    tasks = response.json()
    return render_template('all_tasks.html', tasks=tasks)

@app.route('/api/submit_task', methods=['POST'])
@login_required
def submit_task_api():
    add_task(request.form['description'], [current_user.id])
    return '', 204

@app.route('/api/get_task')
@login_required
def supply_random_task():
    task=get_task([current_user.id])
    return jsonify(task)

@app.route('/api/clear_task/<task_id>', methods=['DELETE'])
@login_required
def clear_task_api(task_id):
    remove_task(task_id)
    return '', 204


@app.route('/api/get_all')
def supply_all_tasks():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    return tasks


    
    
