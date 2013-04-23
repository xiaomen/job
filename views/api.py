import logging
from datetime import date, datetime, timedelta

from flask import Blueprint, request, abort
from utils import *

logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)

@api.route('/')
def index():
    raise abort(404)


@api.route('/job/')
@jsonize
def get_all_jobs_in_feed():
    page = request.args.get('p', '1')
    univ = request.args.get('u', None)
    page = page.isdigit() and int(page) or 1 

    list_page = get_show_jobs(page, per_page=PER_PAGE, fid=univ)

    r = []
    for item in list_page.items:
        if item:
            r.append({'aid': item.id, 'fid': item.fid,
                'title': to_utf8(item.title), 'place': to_utf8(item.place),
                'url': item.url, 'src': item.link })
    d = {'list': r, 'more': not (len(r)<PER_PAGE)}
    return d
