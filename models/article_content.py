from sheep.api.cache import cache

from config import DOMAIN
from models import db

class ArticleContent(db.Model):
    __tablename__ = 'article_content'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    aid = db.Column('aid', db.Integer, nullable=False, index=True)
    fulltext = db.Column('fulltext', db.Text, nullable=True)

    def __init__(self, aid, fulltext):
        self.aid = aid
        self.fulltext = fulltext

def add_article_content(aid, fulltext):
    content = ArticleContent(aid, fulltext)
    db.session.add(content)
    db.session.commit()
    return content

def get_article_content(id):
    return ArticleContent.query.get(id)
