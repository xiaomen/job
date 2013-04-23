#!/usr/bin/python
#coding:utf-8

import json
from functools import wraps

from flask import jsonify

from account import *
from ua import *
from admin import *
from news import *
from rss import *
from query import *
from fulltext import *

json_encoder = json.JSONEncoder()
json_decoder = json.JSONDecoder()

def encode(s):
    return jsonify(s)

def decode(s):
    return json_decoder.decode(s)

def jsonize(f):
    @wraps(f)
    def _(*a, **kw):
        r = f(*a, **kw)
        return encode(r)
    return _

def to_utf8(s):
    return s.encode('utf-8')
