#!/usr/bin/python
#coding:utf-8
import logging
from datetime import datetime

from flask import Blueprint, request, url_for, redirect
from wtforms import Form, TextField, DateTimeField, HiddenField, validators
from wtforms.validators import ValidationError

from models import *
from models.article import get_article
from utils import *
from config import TIME_FORMAT

logger = logging.getLogger(__name__)

admin = Blueprint('admin', __name__)

def validate_date(form, field):
    for f in TIME_FORMAT:
        try:
            d_str = field.data.replace(u'：', ':')
            r = datetime.strptime(d_str.encode('utf-8'), f.encode('utf-8'))
            return True
        except:
            continue
    raise ValidationError('DateTime Format Illegal')

def get_date_from_str(s):
    for f in TIME_FORMAT:
        d_str = s.replace(u'：', ':')
        try:
            return datetime.strptime(d_str.encode('utf-8'), f.encode('utf-8'))
        except:
            continue
    return None

class ArticleForm(Form):
    id = HiddenField('id')
    title = TextField('title', [validators.Required()])
    date = TextField('date', [validators.Required(), validate_date])
    place = TextField('place', [validators.Required()])


@admin.route('/news/<int:id>/delete', methods=['POST'])
@admin_required(need=True, next='http://xiaomen.co/account/register')
def admin_news_delete(id):
    request_url = request.args.get('url', url_for('index'))
    delete_job(id)
    logger.info('{0} delete job {1}.'.format(g.current_user.name, id))

    return redirect(request_url)
    
@admin.route('/news/<int:id>', methods=['GET', 'POST'])
@admin_required(need=True, next='http://xiaomen.co/account/register')
def admin_news(id):
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        article = get_article(form.id.data)
        article.title = form.title.data
        article.date = get_date_from_str(form.date.data)
        article.place = form.place.data
        article.is_published = True
        db.session.add(article)
        db.session.commit()
        logger.info("{0} post data of job {1}.".format(g.current_user.name, id))
        return redirect(url_for('admin.admin_feeds', id=article.fid))

    a = get_article(id)
    fulltext = get_local_fulltext(a.id)
    if a.is_published:
        form.place.data = a.place
        form.date.data = a.date.strftime('%Y-%m-%d %H:%M:%S')
        form.title.data = a.title
    else:
        date, place = get_time_and_place(fulltext)
        form.place.data = (place or u'').strip()
        form.date.data = (date or u'').strip()
        form.title.data = a.title.split()[-1]
    form.id.label = ''
    form.id.data = id
    return render_template('admin.html', form=form, fulltext=fulltext, title=a.title)


@admin.route('/<int:id>')
@admin_required(need=True, next='http://xiaomen.co/account/register')
def admin_feeds(id):
    page = request.args.get('p', '1')
    is_published = 'is_published' in request.args
    if not page or not page.isdigit():
        raise abort(404)
    list_page = get_jobs(page, **dict(fid=id, is_published=is_published))

    return render_template('admin.news.html', fid=id, list_page=list_page, \
            jobs=list_page.items,
            is_published=is_published)

@admin.route('/')
@admin_required(need=True, next='http://xiaomen.co/account/register')
def index():
    feeds = get_feeds()

    return render_template('admin.index.html', feeds=feeds)
