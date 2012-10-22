#!/usr/bin/python
# encoding: UTF-8

import logging
import config

from flask import Flask, render_template, g, request, \
        url_for, redirect

from models import *
from utils import *
from views.admin import admin
from views.news import news

from sheep.api.statics import static_files
from sheep.api.sessions import SessionMiddleware, \
        FilesystemSessionStore
from sheep.api.users import *

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = config.DEBUG
app.jinja_env.filters['s_files'] = static_files

app.jinja_env.globals['generate_user_url'] = generate_user_url
app.jinja_env.globals['generate_login_url'] = generate_login_url
app.jinja_env.globals['generate_logout_url'] = generate_logout_url
app.jinja_env.globals['generate_register_url'] = generate_register_url
app.jinja_env.globals['generate_mail_url'] = generate_mail_url
app.jinja_env.filters['feed_name'] = get_feed_name_of_job

app.config.update(
        SQLALCHEMY_DATABASE_URI = config.DATABASE_URI,
        SQLALCHEMY_POOL_SIZE = 100,
        SQLALCHEMY_POOL_TIMEOUT = 10,
        SQLALCHEMY_POOL_RECYCLE = 3600,
        SESSION_COOKIE_DOMAIN = config.SESSION_COOKIE_DOMAIN,
)

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(news, url_prefix='/news')

init_db(app)

app.wsgi_app = SessionMiddleware(app.wsgi_app, \
        FilesystemSessionStore(), \
        cookie_name=config.SESSION_KEY, \
        cookie_path='/',\
        cookie_domain=config.SESSION_COOKIE_DOMAIN)

@app.route('/')
@check_ua
def index():
    return redirect(url_for('news.index'))

@app.before_request
def before_request():
    g.session = request.environ['xiaomen.session']
    g.current_user = get_current_user(g.session)
    if g.current_user:
        g.unread_mail_count = lambda: get_unread_mail_count(g.current_user.uid)
