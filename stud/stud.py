import sqlite3
from flask import Blueprint, request, flash, render_template, redirect, url_for, session, g
from flask_login import login_required, logout_user, current_user


stud = Blueprint("stud", __name__, template_folder="templates", static_folder="static")

menu = [{'url': '.profile', 'title': 'Профиль'},
        # {'url': '.schedule', 'title': 'Расписание'},
        {'url': '.logout', 'title': 'Выйти'}]


db = None


@stud.before_request
def before_request():
    global db
    db = g.get('link_db')


@stud.teardown_request
def teardown_request(req):
    global db
    db = None
    return req


# def login_stud():
#     session['stud_logged'] = 1
#
#
# def is_logged():
#     return True if session.get("stud_logged") else False
#
#
# def logout_stud():
#     session.pop('stud_logged', None)
#
#
# @stud.route('/')
# def index():
#     if not is_logged():
#         return redirect(url_for(".login"))
#     return render_template("stud/index.html", menu=menu, title="Кабинет волонтёра")

@stud.route("/profile")
@login_required
def profile():
    print("stud profile")
    return render_template("stud/profile.html", menu=menu,
                           title="Профиль ученика", is_auth=current_user.is_authenticated)


@stud.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@stud.route('/schedule')
@login_required
def schedule():
    # dataSeries в виде каледнаря
    return 0
