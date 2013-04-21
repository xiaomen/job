#!/usr/bin/python
#coding:utf-8

import json
from functools import wraps

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
    return json_encoder.encode(s)

def decode(s):
    return json_decoder.decode(s)

def jsonize(f):
    @wraps(f)
    def _(*a, **kw):
        r = f(*a, **kw)
        return encode(r)
    return _

