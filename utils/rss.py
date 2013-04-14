#!/usr/bin/python
#coding:utf-8

import config
import feedparser

from models.article import db, Article
from models.feed import get_all_feeds 

from lib.reader import GoogleReader

def get_rss_from_feed():
    gr = GoogleReader(config.GOOGLE_EMAIL, config.GOOGLE_PASSWD)
    if gr.login():
        feeds = get_all_feeds() 
        for feed in feeds:
            parse_feed(feed.id, gr.get_feed(feed.stream_id))

def parse_feed(fid, rss_feed):
    feed = feedparser.parse(rss_feed)
    for entry in feed.entries:
        if not hasattr(entry, 'summary'):
            entry.summary = ''
        article = Article(fid,
                entry.title,
                entry.published,
                entry.link,
                entry.summary,
                entry.author)
        if Article.query.filter_by(link=entry.link).first():
            break
        db.session.add(article)

    db.session.commit()
