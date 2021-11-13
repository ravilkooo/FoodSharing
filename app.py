import os
import sqlite3
from datetime import datetime

from flask_login import LoginManager, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, g, redirect, flash, url_for
from flask_security import UserMixin, RoleMixin
from FShDataBase import FShDataBase
from UserLogin import UserLogin

DATABASE = '/tmp/site.db'
DEBUG = True
SECRET_KEY = 'adadag4rij9h_w9hfh329q'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'site.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Необходима авторизация"
login_manager.login_message_category = "success"

# app.register_blueprint(admin, url_prefix='/admin')
# app.register_blueprint(coord, url_prefix='/coord')
# app.register_blueprint(volunt, url_prefix='/volunt')
# app.register_blueprint(stud, url_prefix='/stud')


@login_manager.user_loader
def load_user(user_id):
    print("load_user()")
    return UserLogin().from_db(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Conn DB if not"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    """Conn DB before req"""
    global dbase
    db = get_db()
    dbase = FShDataBase(db)


@app.teardown_appcontext
def close_db(error):
    """Disconnect DB"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", title="Главная", menu=dbase.get_guest_menu())


@app.route("/register", methods=("POST", "GET"))
def register():
    return render_template("register.html", title="Регистрация", menu=dbase.get_guest_menu())


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html", menu=dbase.get_guest_menu(), title="Авторизация")
# return render_template("login.html", menu=dbase.get_guest_menu(), title="Авторизация", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", menu=dbase.get_guest_menu(), title="Профиль")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена', menu=dbase.get_guest_menu())


if __name__ == '__main__':
    app.run()
