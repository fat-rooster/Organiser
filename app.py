from flask import Flask, render_template, redirect, url_for, g
from flask_login import LoginManager, current_user
from Models.usermodel import User
from Utilities.Db_utilities import db_build
from settings import SECRET_KEY

app = Flask(__name__, static_url_path = '/Shared/static', template_folder = 'Shared/templates')
app.secret_key = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
conn = db_build()
from Blueprints.Hub import hub

from Blueprints.Login import login, create_users_table
create_users_table(0, conn)

from Blueprints.ToDo import todo, create_tasks_table
create_tasks_table(1, conn)

from Blueprints.Diary import diary, create_diary_entries_table
create_diary_entries_table(2, conn)

conn.close()

app.register_blueprint(login, url_prefix = '/login')
app.register_blueprint(hub, url_prefix = '/user')
app.register_blueprint(todo, url_prefix = '/todo')
app.register_blueprint(diary, url_prefix = '/diary')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/', methods=['GET'])
def home():
    if current_user.is_authenticated:
        return render_template('hub.html')
    return redirect(url_for('Login.login_page'))

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
