import sqlite3
from flask import Blueprint, request, flash, render_template, redirect, url_for, session, g
from flask_login import login_required, logout_user, current_user

from forms import LoginForm

coord = Blueprint("coord", __name__, template_folder="templates", static_folder="static")

menu = [{'url': '.profile', 'title': 'Профиль'},
        # {'url': '.schedule', 'title': 'Расписание'},
        {'url': '.logout', 'title': 'Выйти'}]


db = None


@coord.before_request
def before_request():
    global db
    db = g.get('link_db')


@coord.teardown_request
def teardown_request(req):
    global db
    db = None
    return req


# def login_coord():
#     session['coord_logged'] = 1
#
#
# def is_logged():
#     return True if session.get("coord_logged") else False
#
#
# def logout_coord():
#     session.pop('coord_logged', None)
#
#
# @coord.route('/')
# def index():
#     if not is_logged():
#         return redirect(url_for(".login"))
#     return render_template("coord/index.html", menu=menu, title="Кабинет координатора")


@coord.route("/profile")
@login_required
def profile():
    print("coord profile")
    return render_template("coord/profile.html", menu=menu,
                           title="Профиль координатора", is_auth=current_user.is_authenticated)


@coord.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@coord.route('/schedule')
@login_required
def schedule():
    # dataSeries в виде каледнаря
    return 0
