from sheep.api.cache import cache, backend

from models import db, desc
from utils.cache import npcache

_JOB_FAV_KEY = 'j:f:%s:%s'
_JOB_FAV_ARTICLE = 'j:f:a:%s'

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column('uid', db.Integer, nullable=False)
    aid = db.Column('aid', db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('uid', 'aid', name='_uid_aid'),)

    def __init__(self, uid, aid):
        self.uid = uid
        self.aid = aid

    @classmethod
    @cache(_JOB_FAV_KEY % ('{uid}', '{aid}'))
    def get(cls, uid, aid):
        return cls.query.filter_by(uid=uid, aid=aid).first()

    def delete(self):
        backend.delete(_JOB_FAV_KEY % (self.uid, self.aid))
        db.session.delete(self)
        db.session.commit()
        _flush_favorite(self.uid, self.aid)

def _flush_favorite(uid, aid):
    backend.delete(_JOB_FAV_KEY % (uid, aid))

def _flush_favorite_page(uid):
    backend.delete(_JOB_FAV_ARTICLE % uid)

def get_favorite(uid, aid):
    return Favorite.get(uid=uid, aid=aid)

@npcache(_JOB_FAV_ARTICLE % '{uid}', count=300)
def get_favorite_page(uid, start, limit):
    query = Favorite.query.filter_by(uid=uid).order_by(desc(Favorite.id))
    n = query.count()
    rs = query.offset(start).limit(limit).all()
    return n, rs
