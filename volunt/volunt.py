import sqlite3
from flask import Blueprint, request, flash, render_template, redirect, url_for, session, g

from forms import LoginForm

volunt = Blueprint("volunt", __name__, template_folder="templates", static_folder="static")

menu = [{'url': '.profile', 'title': 'Профиль'},
        {'url': '.schedule', 'title': 'Расписание'},
        {'url': '.logout', 'title': 'Выйти'}]


db = None


@volunt.before_request
def before_request():
    global db
    db = g.get('link_db')


@volunt.teardown_request
def teardown_request(req):
    global db
    db = None
    return req


def login_volunt():
    session['volunt_logged'] = 1


def is_logged():
    return True if session.get("volunt_logged") else False


def logout_volunt():
    session.pop('volunt_logged', None)


@volunt.route('/')
def index():
    if not is_logged():
        return redirect(url_for(".login"))
    return render_template("volunt/index.html", menu=menu, title="Кабинет волонтёра")


@volunt.route('/profile')
def profile():
    return "<p>VOLUNT</p>"