import logging
import unittest
from calendar import timegm
from time import mktime, gmtime
from datetime import datetime
from operator import itemgetter

import feedparser



class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.feedurl_invalid = 'http://www.cnn.com'
        self.feedurl_valid = 'http://rss.cnn.com/rss/cnn_topstories'
        self.past = timegm(gmtime()) - 15000
        self.future = timegm(gmtime()) + 15000

    def test_bad_url_past(self):
        # Make sure an empty dict gets returned for an invalid URL
        test_feed = rssdownload(self.username, self.feedurl_invalid, self.past)
        self.assertTrue(len(test_feed['messages'])==0)

    def test_bad_url_future(self):
        # Make sure an empty dict gets returned for an invalid URL
        test_feed = rssdownload(self.username, self.feedurl_invalid, 
                                self.future)
        self.assertTrue(len(test_feed['messages'])==0)

    def test_good_url_past(self):
        # Make sure an empty dict gets returned for a valid URL
        test_feed = rssdownload(self.username, self.feedurl_valid, self.past)
        self.assertTrue(len(test_feed['messages'])>0, 
                        'Probably no new links found...')

    def test_good_url_future(self):
        # Make sure an empty dict gets returned for a valid URL
        test_feed = rssdownload(self.username, self.feedurl_valid, self.future)
        self.assertTrue(len(test_feed['messages'])==0)

def rssdownload(username, feedurl, last_reference=0, mode=0):
    ''' --> rssdownload(username, feedurl, last_reference=0)

        'username' is used exclusively for logging purposes at this time.
        'feedurl' must be a valid RSS feed. Validation is performed by
        checking the parsed data from the URL for the <title> tag, which
        is RSS 2.0 standard. If feedurl is not a valid RSS URL by that
        standard, an empty dictionary object is returned, and an error is
        logged.

        'last_reference' is a datetime.datetime() of the last time this
        URL was polled. This time is determined by getting the time the
        most recent article was last updated. Only links added or updated
        after last_reference are returned to the user. If there are no
        new links, an error is logged and an empty dictionary object is
        returned.

        mode 0 = default. mode 1 = will search the feed entries for some
        fields commonly used to contain body text. If these fields are
        found, they will be parsed for links, and be returned from this
        function as a separate dictionary object.'''

    messages = []
    feed = feedparser.parse(feedurl)

    logger = logging.getLogger('proxy.rss')
    logger.debug("User %s's update URL is %s" % (username, feedurl))

    if 'title' not in feed.feed:
        logger.error('User %s supplied a URL that does not seem to be a valid R'
                     'SS feed (%s)' %
                     (username, feedurl))
        return {'messages': messages, 'last_reference': last_reference,
                'protected': False}

    for item in feed.entries:
        #feedparser returns timestamp as a time.struct_time object (named
        #tuple) .. the next line converts to datetime.datetime()
        tstamp = datetime.fromtimestamp(mktime((item.updated_parsed)))
        message = {'url': item.link,
                   'timestamp': tstamp,
                   'url_name': item.title}
                        
        messages.append(message)
            
    messages.sort(key = itemgetter('timestamp'))
    last_ref = messages[-1]['timestamp']
   
    return {'messages': messages, 
            'last_reference': last_ref,
            'protected': False}
