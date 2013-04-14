#!/usr/bin/python
#coding:utf-8

from urllib2 import urlopen
from StringIO import StringIO

import re
import logging

from flask import abort
from lxml import etree, html
from models.article_content import get_article_content
from models.favorite import add_favorite, get_favorite

logger = logging.getLogger(__name__)

def get_local_fulltext(aid):
    content = get_article_content(aid) 
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

    doc = html.fromstring(result.decode('gbk'))
    e = doc.find_class('pct')
    if not e:
        return None
    return etree.tostring(e[0])

def get_info_from_pattern(s, p):
    g = re.findall(p, s)
    return g and g[0] or None
    
def get_info(s, patterns):
    for p in patterns:
        d = get_info_from_pattern(s, p)
        if d:
            return d
    return None

def get_time_and_place(fulltext):
    place_patterns = (re.compile(u'>[^<>]*地[址点][：:](?:<[^<>]*>){,5}([^<>]*)[\s<]', re.U), 
            re.compile(u'<td[^<>]*>.*地[址点].*</td><td[^<>]*>(?:<[^<>]*>){,5}([^<>]*)(?:<[^<>]*>){,5}</td>', re.U)
    )
    time_patterns = (re.compile(u'>[^<>]*时间[：:](?:<[^<>]*>){,5}([^<>地]*)[\s<]', re.U), 
            re.compile(u'<td[^<>]*>.*时间[^地]*></td><td[^<>]*>(?:<[^<>]*>){,5}([^<>地]*)(?:<[^<>]*>){,5}</td>', re.U)
    )

    return get_info(fulltext[:2000], time_patterns), \
           get_info(fulltext[:2000], place_patterns)

def decodeHtmlEntity(s) :
    result = s
    entityRe = '(&#(\\d{1,5});)'
    entities = re.findall(entityRe, s)
    for entity in entities :
        result = result.replace(entity[0], unichr(int(entity[1])))
    return result
