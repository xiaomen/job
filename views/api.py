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
    univ = request.args.get('u', '')
    page = page.isdigit() and int(page) or 1 

    if univ:
        list_page = get_all_jobs(page, is_published=True, fid=univ)
    else:
        list_page = get_all_jobs(page, is_published=True)

    r = []
    for item in list_page.items:
        if item:
            r.append({'aid': item.id, 'fid': item.fid,
                'title': item.title, 'place': item.place,
                'url': item.url, 'src': item.link })
    d = {'total': len(list_page.items), 'list': r}
    return d
