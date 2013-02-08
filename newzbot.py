#/usr/bin/env python

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

        time.sleep(60)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >>sys.stderr, """
        Usage: %s <jid> <password>
        """ % sys.argv[0]

    feedlist = ['http://www.heise.de/newsticker/heise-atom.xml',
'http://blog.fefe.de/rss.xml',
'http://www.sueddeutsche.de/app/service/rss/alles/rss.xml',
'http://www.spiegel.de/schlagzeilen/index.rss']
    oldlink = []
    for i in feedlist:
        oldfeed = feedparser.parse(i)
        olditem = oldfeed['entries'][0]['link']
        oldlink.append(olditem)

    username, password = sys.argv[1:]
    newz_bot = NewzBot(username, password, debug=True)
    newz_bot.serve_forever()

