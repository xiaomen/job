#!/usr/bin/python
#coding:utf-8
import logging

from flask import Blueprint, request, url_for, redirect
from wtforms import Form, TextField, DateTimeField, HiddenField, validators

from models import *
from utils import *

logger = logging.getLogger(__name__)

admin = Blueprint('admin', __name__)

class ArticleForm(Form):
    id = HiddenField('id')
    title = TextField('title')
    date = TextField('date')
    place = TextField('place', [validators.Required()])

@admin.route('/<int:id>', methods=['GET', 'POST'])
def admin_index(id):
    form = ArticleForm(request.form)
    a = get_job_by_id(id)
    fulltext = get_local_fulltext(a.id)
    date, place = get_time_and_place(decodeHtmlEntity(fulltext))
    form.place.data = place or u''
    form.date.data = date or u''
    form.title.data = a.title
    form.id.label = ''
    form.id.data = id
    if request.method == 'POST' and form.validate():
        article = get_job_by_id(form.id.data)
        article.date = form.date.data
        article.place = form.place.data
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('admin.admin_index'))

    return render_template('admin.html', form=form, fulltext=fulltext)

@admin.route('/test')
def test():
    id = 22
    a = get_job_by_id(id)
    fulltext = get_fulltext(a.link)
    fulltext = decodeHtmlEntity(fulltext)

    return fulltext
