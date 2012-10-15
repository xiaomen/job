#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time
import config

from flask import Flask
from urllib2 import urlopen
from models import *
from utils import *

logger = logging.getLogger()

app = Flask(__name__)
app.debug = config.DEBUG
app.config.update(
        SQLALCHEMY_DATABASE_URI = 'mysql://',
        SQLALCHEMY_POOL_SIZE = 100,
        SQLALCHEMY_POOL_TIMEOUT = 10,
        SQLALCHEMY_POOL_RECYCLE = 3600
)
init_db(app)

def get_rss_xml(url):
    try:
        res = urlopen(url)
        return res.read()
    except:
        logger.error('open url %s error!' % url)
        return None

def process_feed(f):
    xml = get_rss_xml(f.stream_id)
    if not xml:
        return
    feed = feedparser.parse(xml)
    logger.info(u'fetching rss feed of {0} in {1}'.format(f.name, f.stream_id))
    l = list()
    for entry in feed.entries:
        if not hasattr(entry, 'summary'):
            entry.summary = ''
        if Article.query.filter_by(link=entry.link).first():
            break
        article = Article(f.id, \
                entry.title, \
                entry.published, \
                entry.link, \
                entry.summary, \
                entry.author)
        l.append(article)

    l.reverse()
    for article in l:
        logger.info(u'article {0} of feed {1} has been added to db'.\
                format(article.title, f.name))
        db.session.add(article)
    

def work():
    feeds = Feed.get_feeds()
    for f in feeds:
        process_feed(f)
    db.session.commit()

def main():
    while True:
        work()
        time.sleep(600)

if __name__ == '__main__':
    main()
