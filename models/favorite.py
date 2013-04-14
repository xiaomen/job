from sheep.api.cache import cache

from config import DOMAIN, PER_PAGE
from models import db, IntegrityError
from utils.query import get_article

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column('uid', db.Integer, nullable=False)
    aid = db.Column('aid', db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('uid', 'aid', name='_uid_aid'),)

    def __init__(self, uid, aid):
        self.uid = uid
        self.aid = aid

def add_favorite(uid, aid):
    if not get_article(aid):
        return None

    f = Favorite(uid, aid)
    try:
        db.session.add(f)
        db.session.commit()
    except IntegrityError:
        pass
    return f

def get_favorite(uid, aid):
    return Favorite.query.filter_by(uid=uid, aid=aid).first()

def delete_favorite(uid, aid):
    f = get_favorite(uid, aid)
    if not f:
        return
    db.session.delete(f)
    db.session.commit()

def get_favorite_page(page, per_page, **kw):
    return Favorite.query.filter_by(**kw).paginate(page, per_page=per_page)
