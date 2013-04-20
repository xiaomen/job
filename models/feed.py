# -*- coding:utf-8 -*-

from sheep.api.cache import cache

from config import DOMAIN
from models import db

_JOB_FEED_ALL = 'j:fd:all'
_JOB_FEED_ENABLE = 'j:fd:enable'

class Feed(db.Model):
    __tablename__ = 'feed'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    stream_id = db.Column(db.String(200), nullable=False)
    enabled = db.Column('enabled', db.Boolean, nullable=False, default=True)

    def __init__(self, name, stream_id):
        self.name = name
        self.stream_id = stream_id

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def gets(cls, ids):
        return [cls.get(id) for id in ids]

    @classmethod
    def get_all(cls):
        return cls.query.all()

def get_feed(id):
    return Feed.get(id)

def get_feeds(ids):
    return Feed.gets(ids)

## feed看起来是数量不多变化也不会太大, 并且单个对象所占空间也不大的东西
## 因此直接缓存对象, 不需要因为节约空间而缓存id

@cache(_JOB_FEED_ALL, expire=86400)
def get_all_feeds():
    return Feed.get_all()

@cache(_JOB_FEED_ENABLE, expire=86400)
def get_enabled_feeds():
    return Feed.query.filter_by(enabled=1).all()

def _flush_feeds():
    backend.delete(_JOB_FEED_ALL)
    backend.delete(_JOB_FEED_ENABLE)
