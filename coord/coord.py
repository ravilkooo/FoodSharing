import sqlite3
from flask import Blueprint, request, flash, render_template, redirect, url_for, session, g

from forms import LoginForm

coord = Blueprint("coord", __name__, template_folder="templates", static_folder="static")

menu = [{'url': '.profile', 'title': 'Профиль'},
        {'url': '.schedule', 'title': 'Расписание'},
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


def login_coord():
    session['coord_logged'] = 1


def is_logged():
    return True if session.get("coord_logged") else False


def logout_coord():
    session.pop('coord_logged', None)


@coord.route('/')
def index():
    if not is_logged():
        return redirect(url_for(".login"))
    return render_template("coord/index.html", menu=menu, title="Кабинет волонтёра")


@coord.route('/profile')
def profile():
    return "<p>coord</p>"