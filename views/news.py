import json
import logging

from datetime import date
from datetime import timedelta

from flask import Blueprint, request, abort, \
        render_template, url_for, redirect

from utils import *

logger = logging.getLogger(__name__)

news = Blueprint('news', __name__)

@news.route('/')
def index():
    return get_jobs_in_feed(None)

@news.route('/<int:feed_id>')
def get_jobs_in_feed(feed_id):
    page = request.args.get('p', '1')
    if not page.isdigit():
        raise abort(404)

    feeds = get_feeds()
    if feed_id:
        list_page = get_jobs(page, fid=feed_id)
    else:
        list_page = get_jobs(page)

    today = date.today()
    delta = timedelta(days=1)
    yesterday = today - delta
    day_before = yesterday - delta
    day_before_day = day_before - delta
    return render_template('news.html', list_page = list_page, \
            jobs = list_page.items, \
            feed_id=feed_id, \
            feeds=feeds,
            today = get_point_of_news(today, list_page.items), \
            yesterday = get_point_of_news(yesterday, list_page.items), \
            day_before = get_point_of_news(day_before, list_page.items), \
            day_before_day = get_point_of_news(day_before_day, list_page.items))

@news.route('/favorite', methods=['GET'])
@login_required(need=True, next='http://xiaomen.co/account/register')
def get_favorite_by_user():
    page = request.args.get('p', '1')
    if not page.isdigit():
        raise abort(404)
    list_page = get_favorite_job_by_user(g.current_user.uid, page)

    return render_template('favorite.html', list_page = list_page, \
            jobs = list_page.items)

@news.route('/fulltext/<int:aid>', methods=['GET'])
def fulltext(aid):
    a = get_job_by_id(aid)
    if not a:
        abort(404)
        
    request_url = request.args.get('request_url', None)
    result = get_local_fulltext(aid)
    if not result:
        abort(404)

    if g.current_user:
        f = get_favorite_to_article(g.current_user.uid, aid)
    else:
        f = None
    
    return render_template('fulltext.html', \
            fulltext=result, \
            article=a, \
            favorite=f, \
            request_url=request_url)

@news.route('/fulltext/<int:aid>', methods=['POST'])
@login_required(need=True, next='http://xiaomen.co/account/register')
def favorite(aid):
    a = get_job_by_id(aid)
    action = request.args.get('action', None)
    request_url = request.args.get('request_url', None)
    if not a or not action:
        abort(404)
    
    if action == 'add':
        add_favorite_to_article(g.current_user.uid, aid)
    elif action == 'delete':
        delete_favorite_to_article(g.current_user.uid, aid)
    else:
        abort(400)

    return redirect(url_for('news.fulltext', aid=aid, \
            request_url=request_url))
