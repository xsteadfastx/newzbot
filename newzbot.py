#/usr/bin/env python

import sys
import feedparser
import time
from jabberbot import *


class NewzBot(JabberBot):
    PING_FREQUENCY = 60
    PING_TIMEOUT = 10

    def __init__(self, username, password, debug=True):
        self._timecounter = 1
        super(NewzBot, self).__init__(username, password, debug=True)

    def idle_proc(self):
        self._idle_ping()
        if self._timecounter == 300:
            self._timecounter = 1
            for i in feedlist:
                try:
                    itemposition = feedlist.index(i)

                    new = feedparser.parse(i)
                    newlink = new['entries'][0]['link']

                    if oldlink[itemposition] != newlink:
                        newnews =  new['entries'][0]['title'] + ' ' + new['entries'][0]['link']
                        for contact in self.roster.getRawRoster():
                            self.send(contact, newnews)
                        oldlink[itemposition] = newlink
                except Exception:
                    pass
        else:
            self._timecounter = self._timecounter + 1

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >>sys.stderr, """
        Usage: %s <jid> <password>
        """ % sys.argv[0]

    feedlist = [line.strip() for line in open('./feeds.txt', 'r')]

    oldlink = []
    for i in feedlist:
        try:
            oldfeed = feedparser.parse(i)
            olditem = oldfeed['entries'][0]['link']
            oldlink.append(olditem)
        except Exception:
            oldlink.append('http://google.com')
            pass

    username, password = sys.argv[1:]
    newz_bot = NewzBot(username, password, debug=True)
    newz_bot.serve_forever()

