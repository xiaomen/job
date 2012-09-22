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
        SQLALCHEMY_DATABASE_URI = 'mysql://root:Pa$$w0rd@127.0.0.1:3306/job',
        SQLALCHEMY_POOL_SIZE = 100,
        SQLALCHEMY_POOL_TIMEOUT = 10,
        SQLALCHEMY_POOL_RECYCLE = 3600
)
init_db(app)

def get_rss_xml(url):
    res = urlopen(url)
    return res.read()

def process_feed(f):
    xml = get_rss_xml(f.stream_id)
    feed = feedparser.parse(xml)
    for entry in feed.entries:
        if not hasattr(entry, 'summary'):
            entry.summary = ''
        if Article.query.filter_by(link=entry.link).first():
            break
        article = Article(fid, \
                entry.title, \
                entry.published, \
                entry.link, \
                entry.summary, \
                entry.author)
        print u'article {0} has been added to db'.format(entry.title)
        db.session.add(article)
    

def work():
    feeds = Feed.get_feeds()
    for f in feeds:
        process_feed(f)
        db.session.commit()

def main():
    work()

if __name__ == '__main__':
    main()
