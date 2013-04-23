# -*- coding:utf-8 -*-
import inspect
from functools import wraps

def check_user(f):
    an, v, kw, d = inspect.getargspec(f)
    @wraps(f)
    def _(*a, **kw):
        _a = dict(zip(an, a))
        uid = _a.pop('uid', 0)
        if not uid:
            return dict()
        return f(*a, **kw)
    return _
