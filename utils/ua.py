from functools import wraps

import flask
from flask import request
from werkzeug.useragents import UserAgent

def check_ua(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        ua_string = request.headers.get('User-Agent')
        if not ua_string:
            return method(*args, **kwargs)
        ua = UserAgent(ua_string)
        if ua.browser == 'msie':
            try:
                if int(float(ua.version)) < 8:
                    return render_template("noie.html")
            except:
                return render_template("noie.html")
        return method(*args, **kwargs) 
    return wrapper

def render_template(template_name, *args, **kwargs):
    ua_string = request.headers.get('User-Agent')
    if not ua_string:
        return flask.render_template("mobile/" + template_name, *args, **kwargs) 
    ua = UserAgent(ua_string)
    if ua.platform and ua.platform.lower() in ["android", "iphone"]:
        return flask.render_template("mobile/" + template_name, *args, **kwargs)
    return flask.render_template("mobile/" + template_name, *args, **kwargs)
