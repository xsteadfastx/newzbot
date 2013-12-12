#/usr/bin/env python

import sys
import feedparser
import time
from jabberbot import *


class LittleFeedPoster(object):
    def __init__(self, feed_name, feed_url):
        self.feed_url = feed_url
        self.feed_name = feed_name
        self.old_feed = feedparser.parse(self.feed_url)
        self.old_entry = self.old_feed['entries'][0]['link']

    def has_new_item(self):
        self.new_feed = feedparser.parse(self.feed_url)
        new_entry = self.new_feed['entries'][0]['link']
        if new_entry != self.old_entry:
            self.old_entry = new_entry
            return True
        else:
            return False

    def send_new_item(self):
        if self.has_new_item():
            message = self.new_feed['entries'][0]['title'] + ' ' + self.new_feed['entries'][0]['link']
            return message
        else:
            pass

def read_feed_file(file_name):
    feeds = {}
    with open(file_name, 'r') as feed_list:
        for line in feed_list:
            (key, value) = line.split(' ')
            feeds[key] = value
    return feeds

def generate_feeds(feed_list):
    my_feeds = []
    for key, value in feed_list.items():
        new_feed = LittleFeedPoster(key, value)
        my_feeds.append(new_feed)
    return my_feeds

class NewzBot(JabberBot):
    PING_FREQUENCY = 60
    PING_TIMEOUT = 10

    def __init__(self, username, password, my_feeds):
        self._timecounter = 1
        self.my_feeds = my_feeds
        super(NewzBot, self).__init__(username, password)

    def idle_proc(self):
        self._idle_ping()
        print self._timecounter
        if self._timecounter == 30:
            self._timecounter = 1
            for feed in self.my_feeds:
                message = feed.send_new_item()
                if message is not None:
                    for contact in self.roster.getRawRoster():
                        print contact
                        self.send(contact, message)
        else:
            self._timecounter = self._timecounter + 1

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >>sys.stderr, """
        Usage: %s <jid> <password>
        """ % sys.argv[0]

    my_feed_list = read_feed_file('feeds.list')
    my_feeds = generate_feeds(my_feed_list)

    username, password = sys.argv[1:]
    newz_bot = NewzBot(username, password, my_feeds)
    newz_bot.serve_forever()
