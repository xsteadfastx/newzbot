#/usr/bin/env python

import sys
import feedparser
import time

from jabberbot import *

class NewzBot(JabberBot):
    PING_FREQUENCY = 60
    PING_TIMEOUT = 10

    def idle_proc(self):
        self._idle_ping()
        global timecounter
        try:
            if timecounter == 300:
                timecounter = 1
                for i in feedlist:
                    itemposition = feedlist.index(i)

                    new = feedparser.parse(i)
                    newlink = new['entries'][0]['link']

                    if oldlink[itemposition] != newlink:
                        newnews =  new['entries'][0]['title'] + ' ' + new['entries'][0]['link']
                        for contact in self.roster.getRawRoster():
                            self.send(contact, newnews)
                        oldlink[itemposition] = newlink
            else:
                timecounter = timecounter + 1
        except Exception:
            timecounter = timecounter + 1
            pass

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >>sys.stderr, """
        Usage: %s <jid> <password>
        """ % sys.argv[0]

    timecounter = 1

    feedlist = [line.strip() for line in open('./feeds.txt', 'r')] 

    oldlink = []
    try:
        for i in feedlist:
            oldfeed = feedparser.parse(i)
            olditem = oldfeed['entries'][0]['link']
            oldlink.append(olditem)
    except Exception:
        pass

    username, password = sys.argv[1:]
    newz_bot = NewzBot(username, password, debug=True)
    newz_bot.serve_forever()

