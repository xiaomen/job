#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time
import config
from datetime import datetime

from flask import Flask
from urllib2 import urlopen
from models import *
from utils import *

logger = logging.getLogger()

app = Flask(__name__)
app.debug = config.DEBUG
app.config.update(
        SQLALCHEMY_DATABASE_URI = 'mysql://',
        #SQLALCHEMY_DATABASE_URI = 'mysql://sheep:Sheep4us@106.187.43.13:3306/job',
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
    for entry in feed.entries:
        if not hasattr(entry, 'summary'):
            entry.summary = ''
        logger.info(entry.link)
        if Article.query.filter_by(link=entry.link).first():
            break
        a = Article.create(f.id, \
                entry.title, \
                'todo',
                entry.published, \
                entry.link, \
                entry.summary, \
                entry.author)
        full_text = decodeHtmlEntity(get_fulltext(a.link))
        c = ArticleContent(a.id, full_text)
        db.session.add(c)
        logger.info(u'article {0} of feed {1} has been added to db'.\
                format(a.title, f.name))

def work():
    feeds = Feed.get_feeds()
    for f in feeds:
        try:
            process_feed(f)
        except:
            logger.error('errors occurs when process feed %s' % f.name)
    db.session.commit()

def main():
#    articles = Article.query.all()
#    for article in articles:
#        content =ArticleContent.query.filter_by(aid=article.id).first()
#        if not content:
#            try:
#                full_text = decodeHtmlEntity(get_fulltext(article.link))
#                if not full_text:
#                    print 'error occurs when getting fulltext of {0}'.format(article.id)
#                    continue
#                ArticleContent.create(article.id, full_text)
#                print(u'article {0} content has been added to db'. \
#                        format(article.id))
#            except:
#                print 'error occurs when getting fulltext of {0}'.format(article.id)
#

#    work()
    while True:
        work()
        time.sleep(600)

if __name__ == '__main__':
    main()
