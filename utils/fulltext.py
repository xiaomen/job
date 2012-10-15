from urllib2 import urlopen
from flask import abort

import logging
import lxml.html
from lxml import etree
from models import *

logger = logging.getLogger(__name__)

def get_fulltext(url):
    try:
        f = urlopen(url, timeout=5)
        result = f.read()
    except:
        logger.info('access url %s error' % url)
        return None

    doc = lxml.html.fromstring(result)
    e = doc.find_class('pct')
    if not e or len(e) == 0:
        return None
    return etree.tostring(e[0])

def add_favorite_to_article(uid, aid):
    f = Favorite.get_favorite(uid, aid)
    if not f:
        f = Favorite(uid, aid)
        db.session.add(f)
        db.session.commit()

def delete_favorite_to_article(uid, aid):
    f = Favorite.get_favorite(uid, aid)
    if not f:
        abort(400)
    db.session.delete(f)
    db.session.commit()

def get_favorite_to_article(uid, aid):
    return Favorite.get_favorite(uid, aid)
