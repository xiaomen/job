import logging
from datetime import datetime

from flask import Blueprint, request, abort, \
    render_template, url_for, redirect

from models.article import get_article 
from models.feed import get_enabled_feeds
from models.favorite import get_favorite
from utils import *

logger = logging.getLogger(__name__)

news = Blueprint('news', __name__)


@news.route('/')
def index():
    return get_jobs_in_feed(None)


@news.route('/<int:feed_id>')
def get_jobs_in_feed(feed_id):
    page = request.args.get('p', '1')
    page = page.isdigit() and int(page) or 1

    feeds = get_enabled_feeds()
    if feed_id:
        list_page = get_show_jobs(page, fid=feed_id, is_published=True)
    else:
        list_page = get_all_jobs(page, is_published=True)

    return render_template('news.html', list_page=list_page,
                           jobs=list_page.items or [],
                           feed_id=feed_id,
                           feeds=feeds)


@news.route('/favorite', methods=['GET'])
@login_required(need=True, next='http://xiaomen.co/account/login/')
def get_favorite_by_user():
    page = request.args.get('p', '1')
    page = page.isdigit() and int(page) or 1
    list_page = get_favorite_job_by_user(g.current_user.uid, page)

    return render_template('favorite.html', list_page=list_page,
                           jobs=list_page.items, now=datetime.now())


@news.route('/fulltext/<int:aid>', methods=['GET'])
def fulltext(aid):
    a = get_article(aid)
    if not a:
        abort(404)

    request_url = request.args.get('request_url', None)
    result = get_local_fulltext(aid)
    if not result:
        abort(404)

    if g.current_user:
        f = get_favorite(g.current_user.uid, aid)
    else:
        f = None

    return render_template('fulltext.html',
                           fulltext=result,
                           article=a,
                           favorite=f,
                           request_url=request_url)


@news.route('/fulltext/<int:aid>', methods=['POST'])
@login_required(need=True, next='http://xiaomen.co/account/login/')
def favorite(aid):
    a = get_article(aid)
    action = request.args.get('action', None)
    request_url = request.args.get('request_url', None)
    if not a or not action:
        abort(404)

    if action == 'add':
        a.collect(g.current_user.uid)
    elif action == 'delete':
        a.decollect(g.current_user.uid)
    else:
        abort(400)

    return redirect(url_for('news.fulltext', aid=aid,
                            request_url=request_url))
