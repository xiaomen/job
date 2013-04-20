#!/usr/bin/python
# coding:utf-8

from paginator import Paginator
from models.article import * 
from models.favorite import * 
from models.feed import *
from config import PER_PAGE


def get_all_jobs(page, per_page=PER_PAGE):
    start = (page - 1) * per_page
    n, rs = get_none_intern_articles(start, per_page)
    items = get_articles(rs)
    return Paginator(page, items, per_page=per_page, total=n) 


def get_show_jobs(page, per_page=PER_PAGE, fid=None):
    start = (page - 1) * per_page 
    if fid:
        n, rs = get_feed_articles(start, per_page, fid)
    else:
        n, rs = get_show_articles(start, per_page)
    items = get_articles(rs)
    return Paginator(page, items, per_page=per_page, total=n) 


def get_jobs(page, fid, is_published, per_page=PER_PAGE):
    start = (page - 1) * per_page
    n, rs = get_page(start, per_page, fid, is_published)
    items = get_articles(rs)
    return Paginator(page, items, per_page=per_page, total=n) 


def get_favorite_job_by_user(uid, page):
    page = int(page)
    start = (page - 1) * PER_PAGE
    n, rs = get_favorite_page(uid, start, PER_PAGE)
    items = [get_article(f.aid) for f in rs]
    return Paginator(page, items, per_page=PER_PAGE, total=n) 


def get_jobs_count(fid):
    return get_feed_articles_num(fid)

