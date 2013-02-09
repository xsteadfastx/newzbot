#/usr/bin/env python

import sys
import feedparser
import time
import threading

from jabberbot import *

class NewzBot(JabberBot):

    def thread_proc(self):
        while True:
            for i in feedlist:
                itemposition = feedlist.index(i)

                new = feedparser.parse(i)
                newlink = new['entries'][0]['link']

                if oldlink[itemposition] != newlink:
                    newnews =  new['entries'][0]['title'] + ' ' + new['entries'][0]['link']
                    for contact in self.roster.getRawRoster():
                        self.send(contact, newnews)
                    oldlink[itemposition] = newlink

            time.sleep(60)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >>sys.stderr, """
        Usage: %s <jid> <password>
        """ % sys.argv[0]

    feedlist = ['http://www.heise.de/newsticker/heise-atom.xml',
'http://blog.fefe.de/rss.xml', 'http://rss.bild.de/bild.xml']

    oldlink = []
    for i in feedlist:
        oldfeed = feedparser.parse(i)
        olditem = oldfeed['entries'][0]['link']
        oldlink.append(olditem)

    username, password = sys.argv[1:]
    newz_bot = NewzBot(username, password)
    th = threading.Thread(target = newz_bot.thread_proc)
    newz_bot.serve_forever(th.start())

