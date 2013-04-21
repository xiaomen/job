import inspect
from functools import wraps

from sheep.api.cache import gen_key_factory
from sheep.api.cache import backend

def npcache(key_pattern, count=300, expire=86400):
    def deco(f):
        arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception("do not support varargs")
        if not ('limit' in arg_names):
            raise Exception("function must has 'limit' in args")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)
        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            start = args.pop('start', 0)
            limit = args.pop('limit')
            if not key or limit is None or start+limit > count:
                return f(*a, **kw)

            n = 0
            force = kw.pop('force', False)
            d = backend.get(key) if not force else None
            if d is None:
                n, r = f(start=0, limit=count, **args)
                backend.set(key, (n, r), expire)
            else:
                n, r = d
            return (n, r[start:start+limit])
        _.original_function = f
        return _
    return deco

