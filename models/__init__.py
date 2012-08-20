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
    def get_feed_page(fid, page, per_page):
        result = Article.query.filter(Article.fid==fid) \
                .order_by(desc(Article.pubdate)) \
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
