# -*- coding:utf-8 -*-

from models.favorite import add_favorite
from models.article import get_article

def collect(uid, aid):
    f = add_favorite(uid, aid)
    if not f:
        return dict(r=1, msg='收藏的主题不存在')
    a = get_article(f.aid)
    return dict(r=0, msg='收藏成功')

