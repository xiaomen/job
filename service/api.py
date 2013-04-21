# -*- coding:utf-8 -*-
# init Flask Environment
# init context for service
import app

from utils.query import get_article

def collect(uid, aid):
    article = get_article(aid)
    if not article:
        return dict(r=1, msg='收藏的主题不存在')
    article.collect(uid)
    return dict(r=0, msg='收藏成功')

