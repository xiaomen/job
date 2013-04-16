from sheep.api.cache import cache, backend

from config import DOMAIN, PER_PAGE
from models import db

_JOB_FAV_KEY = 'j:f:%s:%s'

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

    @classmethod
    def paginator(cls, page, per_page, **kw):
        return cls.query.filter_by(**kw).paginate(page, per_page=per_page)

def get_favorite(uid, aid):
    return Favorite.get(uid=uid, aid=aid)

def get_favorite_page(page, per_page, **kw):
    return Favorite.paginator(page, per_page, **kw)
