#/usr/bin/env python

import sys
import feedparser
import time

from jabberbot import *

class NewzBot(JabberBot):

    def idle_proc(self):
        for i in feedlist:
            itemposition = feedlist.index(i)

            new = feedparser.parse(i)
            newlink = new['entries'][0]['link']

            if oldlink[itemposition] != newlink:
                newnews =  new['entries'][0]['title'] + ' ' + new['entries'][0]['link']
                for contact in self.roster.getRawRoster():
                    self.send(contact, newnews)
                oldlink[itemposition] = newlink

        time.sleep(300)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >>sys.stderr, """
        Usage: %s <jid> <password>
        """ % sys.argv[0]

    feedlist = ['http://www.heise.de/newsticker/heise-atom.xml',
'http://blog.fefe.de/rss.xml',
'http://rss.sueddeutsche.de/rss/Eilmeldungen',
'http://www.spiegel.de/schlagzeilen/eilmeldungen/index.rss',
'http://rss.golem.de/rss.php?tp=sec&feed=ATOM1.0']

    oldlink = []
    for i in feedlist:
        oldfeed = feedparser.parse(i)
        olditem = oldfeed['entries'][0]['link']
        oldlink.append(olditem)

    username, password = sys.argv[1:]
    newz_bot = NewzBot(username, password, debug=True)
    newz_bot.serve_forever()

