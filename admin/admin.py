import sqlite3
from flask import Blueprint, request, flash, render_template, redirect, url_for, session, g
from flask_login import login_required, logout_user, current_user


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

menu = [{'url': '.profile', 'title': 'Профиль'},
        # {'url': '.schedule', 'title': 'Расписание'},
        {'url': '.logout', 'title': 'Выйти'}]


db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(req):
    global db
    db = None
    return req


# def login_admin():
#     session['admin_logged'] = 1
#
#
# def is_logged():
#     return True if session.get("admin_logged") else False
#
#
# def logout_admin():
#     session.pop('admin_logged', None)
#
#
# @admin.route('/')
# def index():
#     if not is_logged():
#         return redirect(url_for(".login"))
#     return render_template("admin/index.html", menu=menu, title="Кабинет админа")

@admin.route("/profile")
@login_required
def profile():
    print("admin profile")
    return render_template("admin/profile.html", menu=menu,
                           title="Профиль админа", is_auth=current_user.is_authenticated)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@admin.route('/schedule')
@login_required
def schedule():
    # dataSeries в виде каледнаря
    return 0
