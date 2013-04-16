from datetime import datetime, date

from sheep.api.cache import cache

from config import DOMAIN
from models import db, IntegrityError
from models.favorite import Favorite

_JOB_ARTICEL_KEY = 'j:a:%s'
_JOB_ARTICLE_C_KEY = 'j:ac:%s'

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

    @property
    def body(self):
        a = get_article_content(self.id)
        return a and a.fulltext or ''

    @classmethod
    @cache(_JOB_ARTICEL_KEY % '{id}')
    def get(cls, id):
        return cls.query.get(id)

    @classmethod 
    def gets(cls, ids):
        return [cls.get(i) for i in ids]

    @classmethod
    def create(cls, fid, title, place, pubdate, link, description, author):
        article = cls(fid, title, place, pubdate, link, description, author)
        db.session.add(article)
        db.session.commit()
        return article

    def collect(self, uid):
        f = Favorite(uid, self.id)
        try:
            db.session.add(f)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return f

    def decollect(self, uid):
        from utils.query import get_favorite
        f = get_favorite(uid, self.id)
        if not f:
            return
        f.delete()

class ArticleContent(db.Model):
    __tablename__ = 'article_content'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    aid = db.Column('aid', db.Integer, nullable=False, index=True)
    fulltext = db.Column('fulltext', db.Text, nullable=True)

    def __init__(self, aid, fulltext):
        self.aid = aid
        self.fulltext = fulltext

    @classmethod
    @cache(_JOB_ARTICLE_C_KEY % '{aid}')
    def get(cls, aid):
        return cls.query.get(aid)

    @classmethod
    def create(cls, aid, fulltext):
        content = cls(aid, fulltext)
        try:
            db.session.add(content)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return content

def add_article_content(aid, fulltext):
    return ArticleContent.create(aid, fulltext)

def get_article_content(aid):
    return ArticleContent.get(aid)

def add_article(fid, title, place, pubdate, link, description, author):
    return Article.create(fid, title, place, pubdate, link, description, author)

def get_article(id):
    return Article.get(id)

def get_articles(ids):
    return Article.gets(ids)

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
