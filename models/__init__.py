from datetime import datetime

from sqlalchemy.sql.expression import desc
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    db.app = app
    db.create_all()

class Feed(db.Model):
    __tablename__ = 'feed'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    stream_id = db.Column(db.String(200), nullable=False)

    def __init__(self, name, stream_id):
        self.name = name
        self.stream_id = stream_id

    @staticmethod
    def get_feeds():
        return Feed.query.all()

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    fid = db.Column('fid', db.Integer, nullable=False, index=True)
    title = db.Column(db.String(100), nullable=False)
    pubdate = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    author = db.Column(db.String(100), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, fid, title, pubdate, link, description, author):
        self.fid = fid
        self.title = title
        self.pubdate = pubdate
        self.link = link
        self.description = description
        self.author = author

    @staticmethod
    def create(fid, title, pubdate, link, description, author):
        article = Article(fid, title, pubdate, link, description, author)
        db.session.add(article)
        db.session.commit()

    @staticmethod
    def get_page(page, per_page, **kw):
        result = Article.query.filter_by(**kw) \
                .order_by(desc(Article.created)) \
                .paginate(page, per_page=per_page)
        return result

class ArticleContent(db.Model):
    __tablename__ = 'article_content'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    aid = db.Column('aid', db.Integer, nullable=False, index=True)
    fulltext = db.Column('fulltext', db.Text, nullable=True)

    def __init__(self, aid, fulltext):
        self.aid = aid
        self.fulltext = fulltext

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column('uid', db.Integer, nullable=False)
    aid = db.Column('aid', db.Integer, nullable=False)

    def __init__(self, uid, aid):
        self.uid = uid
        self.aid = aid

    @staticmethod
    def create_favorite(uid, aid):
        f = Favorite(uid, aid)
        db.session.add(f)
        db.session.commit()

    @staticmethod
    def get_favorite(uid, aid):
        return Favorite.query.filter_by(uid=uid, aid=aid).first()

    @staticmethod
    def delete_favorite(uid, aid):
        f = get_favorite(uid, aid)
        if not f:
            return
        db.delete(f)
        db.session.commit()
