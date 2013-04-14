from models import *
from models.feed import get_feed

def get_point_of_news(d, news):
    for new in news:
        if new.created.date() == d:
            return new
    return None

def get_feed_name_of_job(job):
    f = get_feed(job.fid)
    name = f and f.name or ''
    return name 

