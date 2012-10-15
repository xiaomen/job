import json
import logging

from flask import Blueprint, request, abort, render_template

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

    return render_template('news.html', list_page = list_page, \
            jobs = list_page.items, \
            feed_id=feed_id, \
            feeds=feeds)

@news.route('/fulltext/<int:aid>')
def fulltext(aid):
    feed_id = request.args.get('fid', None)
    a = get_job_by_id(aid)
    url = a.link
    result = get_fulltext(url)
    return render_template('fulltext.html', fulltext=result, \
            feed_id=feed_id)
