#!/usr/bin/python
#coding:utf-8

from datetime import datetime, date

from flask import abort

from utils.query import get_article

def delete_job(id):
    job = get_article(id)
    if not job:
        abort(404)
    db.session.delete(job)
    db.session.commit()
