from functools import wraps
from flask import g, url_for, redirect, request

def login_required(next=None, need=True, *args, **kwargs):
    def _login_required(f):
        @wraps(f)
        def _(*args, **kwargs):
            if (need and not g.current_user) or \
                    (not need and g.current_user):
                if next:
                    return redirect(next)
                return redirect('/')
            return f(*args, **kwargs)
        return _
    return _login_required
