import logging

from flask import Blueprint

from utils import *

logger = logging.getLogger(__name__)

admin = Blueprint('admin', __name__)

@admin.route('/', methods=['GET'])
def admin_index():
    get_rss_from_feed()
    return 'Yes!'
