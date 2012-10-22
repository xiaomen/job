#!/usr/bin/python
#coding:utf-8

from flask import abort
from models import *
from datetime import datetime, date

def delete_job(id):
    job = Article.query.get(id)
    if not job:
        abort(404)
    db.session.delete(job)
    db.session.commit()
