# -*- coding:utf-8 -*-
# init Flask Environment
# init context for service
from datetime import datetime

import app

from utils.query import get_article, get_favorite_job_by_user, get_feed, get_show_jobs
from service import check_user

_INTERN = 1

@check_user
def collect(uid, aid):
    article = get_article(aid)
    if not article:
        return dict(r=1, msg='收藏的主题不存在')
    article.collect(uid)
    return dict(r=0, msg='收藏成功')

@check_user
def favorite(uid, page):
    list_page = get_favorite_job_by_user(uid, page)
    return __job_to_dict(list_page)

@check_user
def detail(uid, aid):
    article = get_article(aid)
    if not article:
        return dict()
    feed = get_feed(article.fid)
    return dict(aid=article.id, feed=feed.name,
            date=article.date.strftime('%Y-%m-%d %H:%M'),
            expired=(datetime.now() > article.date), place=article.place,
            pubdate=article.pubdate, link=article.link, text=article.body)

@check_user
def list_jobs(uid, page, fid=None):
    list_page = get_show_jobs(page, fid=fid)
    return __job_to_dict(list_page)

@check_user
def list_interns(uid, page):
    list_page = get_show_jobs(page, fid=_INTERN)
    return __job_to_dict(list_page)
    

def __job_to_dict(list_page):
    rs = []
    for item in list_page.items:
        r = dict(aid=item.id, title=item.title,
                date=item.date.strftime('%Y-%m-%d %H:%M'),
                expired=(datetime.now() > item.date), place=item.place)
        rs.append(r)
    return dict(rs=rs, total=list_page.total, more=list_page.has_next)

