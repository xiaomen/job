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

def get_feed(id):
    return Feed.query.get(id)

def get_feeds(ids):
    return Feed.query.filter(Feed.id.in_(ids)).all()

def get_all_feeds():
    return Feed.query.all()

def get_enabled_feeds():
    return Feed.query.filter_by(enabled=1)

