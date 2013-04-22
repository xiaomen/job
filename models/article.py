# -*- coding:utf-8 -*-

from datetime import datetime, date

from sheep.api.cache import cache, backend

from config import DOMAIN
from utils.cache import npcache
from models import db, desc, IntegrityError
from models.favorite import Favorite, _flush_favorite_page

_JOB_ARTICEL_KEY = 'j:a:%s'
_JOB_ARTICLE_C_KEY = 'j:ac:%s'
_JOB_SHOW_ARTICLES = 'j:a:q:show'
_JOB_NONE_INTERN_ARTICLES = 'j:a:q:noneintern'
_JOB_FEED_ARTICLES = 'j:a:f:%s'
_JOB_ALL_ARTICLES = 'j:a:all:%s:%s'
_JOB_FEED_COUNT = 'j:a:fc:%s'

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
    @cache(_JOB_ARTICEL_KEY % '{id}', expire=86400)
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def gets(cls, ids):
        return [cls.get(i) for i in ids]

    @classmethod
    def get_ids(cls):
        '''这个方法纯粹为了缓存, Article很大而且获取单个实例会比较频繁,
        所以把id缓存起来, 再从缓存里按照id取实例会比较划算'''
        return db.session.query(Article.id)

    @classmethod
    def create(cls, fid, title, place, pubdate, link, description, author):
        article = cls(fid, title, place, pubdate, link, description, author)
        db.session.add(article)
        db.session.commit()
        _flush_article_page(fid)
        return article

    def collect(self, uid):
        f = Favorite(uid, self.id)
        try:
            db.session.add(f)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        _flush_favorite_page(uid)
        return f

    def decollect(self, uid):
        from utils.query import get_favorite
        f = get_favorite(uid, self.id)
        if not f:
            return
        f.delete()
        _flush_favorite_page(uid)

    def delete(self):
        urs = db.session.query(Favorite.uid).filter_by(aid=self.id).all()

        db.session.delete(self)
        db.session.query(Favorite).filter_by(aid=self.id).delete()
        db.session.query(ArticleContent).filter_by(aid=self.id).delete()
        db.session.commit()

        _flush_article_content(self.id)
        _flush_article_page(self.fid)
        ## TODO 这个写法是有点奇怪, 但是现在的数据表结构只能这么做=.=
        ## 如果这个urs很大怎么搞... 是个问题... 要想一下
        [_flush_favorite_page(uid) for uid in urs]

    def update(self, title, date, place, is_published):
        self.title = title
        self.date = date
        self.place = place
        self.is_published = is_published
        db.session.add(self)
        db.session.commit()
        _flush_article_page(self.fid)

class ArticleContent(db.Model):
    __tablename__ = 'article_content'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    aid = db.Column('aid', db.Integer, nullable=False, index=True)
    fulltext = db.Column('fulltext', db.Text, nullable=True)

    def __init__(self, aid, fulltext):
        self.aid = aid
        self.fulltext = fulltext

    @classmethod
    @cache(_JOB_ARTICLE_C_KEY % '{aid}', expire=86400)
    def get(cls, aid):
        return cls.query.filter_by(aid=aid).first()

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

@npcache(_JOB_SHOW_ARTICLES, count=300)
def get_show_articles(start, limit):
    query = get_article_ids_by(is_published=True).filter(
        'date>now() and fid in (select id from feed where enabled=1)').order_by(desc(Article.date))
    rs = query.offset(start).limit(limit).all()
    n = query.count()
    return n, rs

@npcache(_JOB_NONE_INTERN_ARTICLES, count=300)
def get_none_intern_articles(start, limit):
    query = get_article_ids_by(is_published=True).filter(
        'fid<>1 and date>now() and fid in (select id from feed where enabled=1)').order_by(desc(Article.date))
    rs = query.offset(start).limit(limit).all()
    n = query.count()
    return n, rs

@npcache(_JOB_FEED_ARTICLES % '{fid}', count=300)
def get_feed_articles(start, limit, fid):
    query = get_article_ids_by(
        is_published=True, fid=fid).order_by(desc(Article.date))
    rs = query.offset(start).limit(limit).all()
    n = query.count()
    return n, rs

@npcache(_JOB_ALL_ARTICLES % ('{fid}', '{is_published}'), count=300)
def get_page(start, limit, fid, is_published):
    query = get_article_ids_by(
        fid=fid, is_published=is_published).order_by(desc(Article.date))
    rs = query.offset(start).limit(limit).all()
    n = query.count()
    return n, rs

@cache(_JOB_FEED_COUNT % '{fid}', expire=86400)
def get_feed_articles_num(fid):
    return get_article_ids_by(fid=fid).count()

def get_article_by(**kw):
    return Article.query.filter_by(**kw)

def get_article_ids_by(**kw):
    return Article.get_ids().filter_by(**kw)

def _flush_article_page(fid):
    backend.delete(_JOB_SHOW_ARTICLES)
    backend.delete(_JOB_NONE_INTERN_ARTICLES)
    backend.delete(_JOB_FEED_ARTICLES % fid)
    # TODO 这样写真的很奇怪...但是这货的is_published属性是在数据库直接set的...
    # 刚刚create的时候都没得, 删除的时候也不一定有, 所以都flush掉
    # 这样很挫, 应该想个什么策略...
    backend.delete(_JOB_ALL_ARTICLES % (fid, True))
    backend.delete(_JOB_ALL_ARTICLES % (fid, False))
    backend.delete(_JOB_FEED_COUNT % fid)

def _flush_article_content(aid):
    backend.delete(_JOB_ARTICLE_C_KEY % aid)
