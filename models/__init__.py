from datetime import datetime, date

from sqlalchemy.sql.expression import desc
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_today():
    t = date.today()
    return datetime(t.year, t.month, t.day)

def init_db(app):
    db.init_app(app)
    db.app = app
    db.create_all()

class Feed(db.Model):
    __tablename__ = 'feed'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    stream_id = db.Column(db.String(200), nullable=False)
    enabled = db.Column('enabled', db.Boolean, nullable=False, default=True)

    def __init__(self, name, stream_id):
        self.name = name
        self.stream_id = stream_id

    @staticmethod
    def get_feeds(**kw):
        return Feed.query.all()

    @staticmethod
    def get_enabled_feeds():
        return Feed.query.filter_by(enabled=1)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    fid = db.Column('fid', db.Integer, nullable=False, index=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now, nullable=True)
    place = db.Column(db.String(100), nullable=True)
    pubdate = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    author = db.Column(db.String(100), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, fid, title, place, \
            pubdate, link, description, author):
        self.fid = fid
        self.title = title
        self.place = place
        self.pubdate = pubdate
        self.link = link
        self.description = description
        self.author = author

    @staticmethod
    def create(fid, title, place, pubdate, link, description, author):
        article = Article(fid, title, place, pubdate, \
                link, description, author)
        db.session.add(article)
        db.session.commit()
        return article

    @staticmethod
    def get_query_page(page, per_page, **kw):
        result = Article.query.filter_by(**kw) \
                .filter('date>now() and fid in (select id from feed where enabled=1)') \
                .order_by(Article.date) \
                .paginate(page, per_page=per_page)
        return result

    @staticmethod
    def get_page(page, per_page, **kw):
        result = Article.query.filter_by(**kw) \
                .order_by(desc(Article.date)) \
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

    @staticmethod
    def create(aid, fulltext):
        content = ArticleContent(aid, fulltext)
        db.session.add(content)
        db.session.commit()

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
