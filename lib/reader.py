import logging

from time import time
from urllib import urlencode, quote_plus
from urllib2 import urlopen, Request

LOGIN_URL = 'https://www.google.com/accounts/ClientLogin'
TOKEN_URL = 'https://www.google.com/reader/api/0/token'
SUBSCRIBE_URL = 'https://www.google.com/reader/api/0/subscription/quickadd?output=json'
FEED_URL = 'https://www.google.com/reader/atom/feed'

logger = logging.getLogger(__name__)

class GoogleReader(object):

    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd

    def login(self):
        request = Request(LOGIN_URL, urlencode({
            'service': 'reader',
            'Email': self.email,
            'Passwd': self.passwd,
            'source': 'xiaomenco'
        }))

        try:
            f = urlopen(request, timeout=5)
            lines = f.read().split()
            self.auth = lines[2][5:]
        except:
            logger.info('login to GoogleReader fail')
            return False

        return True

    def get_token(self):
        headers = {'Authorization': 'GoogleLogin auth=' + self.auth}
        request = Request(TOKEN_URL, headers=headers)
        try:
            f = urlopen(request, timeout=5)
            token = f.read()
            self.token = token
        except:
            logger.info('get token error.')
            return None
        return token

    def subscribe(self, feed):
        headers = {'Authorization': 'GoogleLogin auth=' + self.auth}
        request = Request(SUBSCRIBE_URL, urlencode({
            'quickadd': feed,
            'T': self.get_token()}), headers=headers)
        try:
            f = urlopen(request, timeout=5)
            return f.read()
        except:
            logger.info('subscribe %s error' % feed)
            return None

    def get_feed(self, feed, num=100):
        headers = {'Authorization': 'GoogleLogin auth=' + self.auth}
        request = Request(FEED_URL + \
                quote_plus('/' + feed) + \
                '?n=%d' % num, headers=headers)

        try:
            f = urlopen(request, timeout=10)
            return f.read()
        except:
            logger.info('get feed %s error' %feed)
            return None
