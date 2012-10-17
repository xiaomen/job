def get_point_of_news(d, news):
    for new in news:
        if new.created.date() == d:
            return new
    return None
