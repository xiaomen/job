#!/usr/bin/python
# coding:utf-8

from paginator import gen_list_paginator
from models import *
from models.article import * 
from models.favorite import get_favorite_page
from config import PER_PAGE


def get_all_jobs(page, **kw):
    page = int(page)
    paginator = get_query_page_without_intern(
        page, per_page=PER_PAGE, **kw)
    return gen_list_paginator(paginator)


def get_show_jobs(page, **kw):
    page = int(page)
    paginator = get_query_page(page, per_page=PER_PAGE, **kw)
    return gen_list_paginator(paginator)


def get_jobs(page, **kw):
    page = int(page)
    paginator = get_page(page, per_page=PER_PAGE, **kw)
    return gen_list_paginator(paginator)


def get_favorite_job_by_user(uid, page):
    page = int(page)
    paginator = get_favorite_page(page, PER_PAGE, uid=uid)
    paginator.items = [get_article(f.aid) for f in paginator.items]
    return gen_list_paginator(paginator)


def get_jobs_count(fid):
    return get_article_by(fid=fid).count()

