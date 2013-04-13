#!/usr/bin/python
# coding:utf-8


class Paginator(object):
    def __init__(self, page_obj):
        if page_obj:
            for name in dir(page_obj):
                if not name.startswith('_'):
                    setattr(self, name, getattr(page_obj, name))
            setattr(self, 'iter_pages', xrange(1, page_obj.pages + 1))
        else:
            self.items = []
            self.has_next = self.has_prev = False
            self.next_num = self.total = 0
            self.page = 0
            self.pages = 0
            self.iter_pages = None


def gen_list_page_obj(page_obj):
    return Paginator(page_obj)
