#!/usr/bin/python
#coding:utf-8

from urllib2 import urlopen
from flask import abort

import re
import logging
import lxml.html
from lxml import etree
from models import *
from StringIO import StringIO

logger = logging.getLogger(__name__)

def get_local_fulltext(id):
    content = ArticleContent.query.get(id)
    if not content:
        return None
    return content.fulltext

def get_fulltext(url):
    try:
        f = urlopen(url, timeout=5)
        result = f.read()
    except:
        logger.info('access url %s error' % url)
        return None

    doc = lxml.html.fromstring(result.decode('gbk'))
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

def get_info_from_pattern(s, p):
    g = re.findall(p, s)
    if not g or len(g) == 0 or len(g[0]) == 0:
        return None
    return g[0]
    
def get_info(s, patterns):

    for p in patterns:
        d = get_info_from_pattern(s,p)
        if d:
            return d
    return None

def get_time_and_place(fulltext):
    place_patterns = [re.compile(u'>[^<>]*地[址点][：:]([^<>]*)[\s<]', re.U), \
            re.compile(u'<td[^<>]*>.*地[址点].*</td><td[^<>]*>(?:<[^<>]*>)([^<>]*)(?:<[^<>]*>)</td>', re.U)
    ]
    time_patterns = [re.compile(u'>[^<>]*时间[：:]([^<>地]*)[\s<]', re.U), \
            re.compile(u'<td[^<>]*>.*时间[^地]*><td[^<>]*>(?:<[^<>]*>)([^<>地]*)(?:<[^<>]*>)</td>', re.U)
    ]

    return get_info(fulltext, time_patterns), \
           get_info(fulltext, place_patterns)

def decodeHtmlEntity(s) :
    result = s
    entityRe = '(&#(\\d{1,5});)'
    entities = re.findall(entityRe, s)
    for entity in entities :
        result = result.replace(entity[0], unichr(int(entity[1])))
    return result
