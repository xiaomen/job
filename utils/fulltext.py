from urllib2 import urlopen

import logging
import lxml.html
from lxml import etree

logger = logging.getLogger(__name__)

def get_fulltext(url):
    try:
        f = urlopen(url, timeout=5)
        result = f.read()
    except:
        logger.info('access url %s error' % url)
        return None

    doc = lxml.html.fromstring(result)
    e = doc.find_class('pct')
    if not e or len(e) == 0:
        return None
    return etree.tostring(e[0])
