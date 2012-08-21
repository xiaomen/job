import json
import logging

from flask import Blueprint, request, abort, render_template

from utils import *

logger = logging.getLogger(__name__)

news = Blueprint('news', __name__)

@news.route('/')
def index():
    feeds = get_feeds()
    return render_template('index.html', feeds=feeds)

@news.route('/<int:feed_id>')
def get_jobs_in_feed(feed_id):
    page = request.args.get('p', '1')
    if not page.isdigit():
        raise abort(404)

    list_page = get_jobs(feed_id, page)

    return render_template('news.html', list_page = list_page, \
            jobs = list_page.items, \
            feed_id=feed_id)

@news.route('/fulltext/<int:aid>')
def fulltext(aid):
    a = get_job_by_id(aid)
    url = a.link
    result = get_fulltext(url)
    if not a.link:
        return 'None'
    return result
