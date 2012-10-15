#!/usr/bin/python
#coding:utf-8

from helper import gen_list_page_obj

from models import *

from config import PAGE_NUM

def get_feeds():
    return Feed.get_feeds()

def get_jobs(page, **kw):
    page = int(page)
    page_obj = Article.get_page(page, per_page=PAGE_NUM, **kw)
    return gen_list_page_obj(page_obj)

def get_job_by_id(aid):
    return Article.query.get(aid)

def get_jobs_count(fid):
    return get_job_by(fid=fid).count()

def get_job_by(**kw):
    return Article.query.filter_by(**kw)
