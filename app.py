import os
import sqlite3
from datetime import datetime

from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, g, redirect, flash, url_for, make_response
from flask_security import UserMixin, RoleMixin
from FShDataBase import FShDataBase
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm
from volunt.volunt import volunt
from coord.coord import coord
from admin.admin import admin



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

app.register_blueprint(coord, url_prefix='/coord')
app.register_blueprint(volunt, url_prefix='/volunt')
app.register_blueprint(admin, url_prefix='/admin')


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
    print(dbase.get_guest_menu())
    return render_template("index.html", title="Главная",
                           menu=dbase.get_guest_menu(), is_auth=current_user.is_authenticated)


@app.route("/register", methods=("POST", "GET"))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegisterForm()
    if form.validate_on_submit():
        hpsw = generate_password_hash(form.psw.data)
        res = dbase.add_user(form.name.data, form.surname.data, form.email.data, hpsw)
        if res:
            flash("Вы успешно зарегестрированы", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", "error")
    return render_template("register.html", title="Регистрация", menu=dbase.get_guest_menu(),
                           form=form, is_auth=current_user.is_authenticated)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.get_user_by_email(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            user_login = UserLogin().create(user)
            rm = form.remember.data
            login_user(user_login, remember=rm)
            role = dbase.get_role(user['id'])
            if (role == 'guest') or (role == 'stud'):
                return redirect(request.args.get('next') or url_for('profile'))
            return redirect(url_for(role+'.profile'))
        flash("Неверный логин или пароль", "error")
    return render_template("login.html", menu=dbase.get_guest_menu(),
                           title="Авторизация", form=form, is_auth=current_user.is_authenticated)


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", menu=dbase.get_guest_menu(),
                           title="Профиль", is_auth=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/userava')
@login_required
def userava():
    img = current_user.get_avatar(app)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verify_ext(file.filename):
            try:
                img = file.read()
                res = dbase.update_user_avatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка обновления аватара", "error")
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "error")
    return redirect(url_for('profile'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена', menu=dbase.get_guest_menu())


if __name__ == '__main__':
    app.run()
