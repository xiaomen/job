from sheep.api.cache import cache

from config import DOMAIN
from models import db

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

def get_all_feeds():
    return Feed.get_all()

def get_enabled_feeds():
    return Feed.query.filter_by(enabled=1)

