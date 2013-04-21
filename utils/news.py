from utils.query import get_feed

def get_point_of_news(d, news):
    for n in news:
        if n.created.date() == d:
            return n
    return None

def get_feed_name_of_job(job):
    f = get_feed(job.fid)
    name = f and f.name or ''
    return name 

