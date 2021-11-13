import sqlite3
from flask import Blueprint, request, flash, render_template, redirect, url_for, session, g

volunt = Blueprint("volunt", __name__, template_folder="templates", static_folder="static")

menu = [{'url': '.index', 'title': 'Панель'},
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




