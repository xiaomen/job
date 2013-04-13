import logging
from datetime import date, datetime, timedelta

from flask import Blueprint, request, abort, \
    render_template, url_for, redirect
from utils import *

logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)

@api.route('/')
def index():
    raise abort(404)


@api.route('/job')
@jsonize
def get_all_jobs_in_feed():
    page = request.args.get('p', '1')
    if not page.isdigit():
        raise abort(404)

    list_page = get_all_jobs(page, is_published=True)
    r = []
    for item in list_page.items:
        if item:
            r.append({'id': item.id, 'fid': item.fid,
                      'title': item.title})
    d = {'total': list_page and len(list_page.items),
         'list': r}
    return d
