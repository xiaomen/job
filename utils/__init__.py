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
from helper import *
from fulltext import *

json_encoder = json.JSONEncoder()

def encode(s):
    return json_encoder.encode(s)

def jsonize(f):
    @wraps(f)
    def _(*a, **kw):
        r = f(*a, **kw)
        return encode(r)
    return _

