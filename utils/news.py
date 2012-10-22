from models import *

def get_point_of_news(d, news):
    for new in news:
        if new.created.date() == d:
            return new
    return None

def get_feed_name_of_job(job):
    f = Feed.query.get(job.fid)
    if f:
        return f.name
    return ''

