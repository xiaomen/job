#!/usr/bin/python
#coding:utf-8

from helper import gen_list_page_obj

from models import *

from config import PAGE_NUM

def get_jobs(fid, page):
    page = int(page)
    page_obj = Article.get_feed_page(fid, page, per_page=PAGE_NUM)
    return gen_list_page_obj(page_obj)

def get_jobs_count(fid):
    return get_job_by(fid=fid).count()

def get_job_by(**kw):
    return Article.query.filter_by(**kw)
