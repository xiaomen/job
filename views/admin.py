#!/usr/bin/python
#coding:utf-8
import logging
from datetime import datetime

from flask import Blueprint, request, url_for, redirect
from wtforms import Form, TextField, DateTimeField, HiddenField, validators
from wtforms.validators import ValidationError

from models import *
from utils import *
from config import TIME_FORMAT

logger = logging.getLogger(__name__)

admin = Blueprint('admin', __name__)

def validate_date(form, field):
    try:
        datetime.strptime(field.data, TIME_FORMAT)
    except:
        raise ValidationError('DateTime Format Illegal')

def get_date_from_str(s):
    return datetime.strptime(s, TIME_FORMAT)

class ArticleForm(Form):
    id = HiddenField('id')
    title = TextField('title', [validators.Required()])
    date = TextField('date', [validators.Required(), validate_date])
    place = TextField('place', [validators.Required()])


@admin.route('/news/<int:id>', methods=['GET', 'POST'])
def admin_news(id):
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        article = get_job_by_id(form.id.data)
        article.title = form.title.data
        article.date = get_date_from_str(form.date.data)
        article.place = form.place.data
        article.is_published = True
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('admin.admin_feeds', id=article.fid))

    a = get_job_by_id(id)
    fulltext = get_local_fulltext(a.id)
    date, place = get_time_and_place(decodeHtmlEntity(fulltext))
    form.place.data = place or u''
    form.date.data = date or u''
    form.title.data = a.title.split()[-1]
    form.id.label = ''
    form.id.data = id
    return render_template('admin.html', form=form, fulltext=fulltext, title=a.title)


@admin.route('/<int:id>')
def admin_feeds(id):
    page = request.args.get('p', '1')
    if not page or not page.isdigit():
        raise abort(404)
    list_page = get_jobs(page, **dict(fid=id, is_published=False))

    return render_template('admin.news.html', fid=id, list_page=list_page, \
            jobs=list_page.items)

@admin.route('/')
def index():
    feeds = get_feeds()

    return render_template('admin.index.html', feeds=feeds)
