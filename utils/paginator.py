#!/usr/bin/python
# coding:utf-8
from math import ceil

from config import PER_PAGE

class Paginator(object):
    '''
    分页器, page第几页(从1开始), items所有的item, per_page每页个数
    total 总数
    '''
    def __init__(self, page, items, per_page=PER_PAGE, total=None):
        self.items = items
        self.total = total or 0
        self.page = page
        self.per_page = per_page
        if total is None:
            # 当这一次取出来不够per_page了就认为没有了,
            # 实际是有问题的, 最后一页刚好取完的话会取两次
            self.has_next = not (len(items) < per_page)
        else:
            # 如果有total值就可以用total来算了
            self.has_next = page * self.per_page < total

    @property
    def pages(self):
        return int(ceil(self.total / float(self.per_page)))

    @property
    def prev(self):
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def next_num(self):
        return self.page + 1

    def iter_pages(self):
        return xrange(1, self.pages + 1)

