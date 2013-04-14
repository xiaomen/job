from datetime import datetime, date

from sheep.api.cache import cache

from config import DOMAIN
from models import db

def get_today():
    t = date.today()
    return datetime(t.year, t.month, t.day)

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

    def __init__(self, fid, title, place, 
            pubdate, link, description, author):
        self.fid = fid
        self.title = title
        self.place = place
        self.pubdate = pubdate
        self.link = link
        self.description = description
        self.author = author

    @property
    def url(self):
        return '%s/news/fulltext/%s' % (DOMAIN, self.id)

def add_article(fid, title, place, pubdate, link, description, author):
    article = Article(fid, title, place, pubdate, link, description, author)
    db.session.add(article)
    db.session.commit()
    return article

def get_article(id):
    return Article.query.get(id)

def get_articles(ids):
    return Article.query.filter(Article.id.in_(ids)).all()

def get_query_page(page, per_page, **kw):
    result = get_article_by(**kw) \
            .filter('date>now() and fid in (select id from feed where enabled=1)') \
            .order_by(Article.date) \
            .paginate(page, per_page=per_page)
    return result

def get_query_page_without_intern(page, per_page, **kw):
    result = get_article_by(**kw) \
            .filter('fid<>1 and date>now() and fid in (select id from feed where enabled=1)') \
            .order_by(Article.date) \
            .paginate(page, per_page=per_page)
    return result

def get_page(page, per_page, **kw):
    result = get_article_by(**kw) \
            .order_by(desc(Article.date)) \
            .paginate(page, per_page=per_page)
    return result

def get_article_by(**kw):
    return Article.query.filter_by(**kw)
