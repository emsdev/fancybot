import urllib
from api import *


class Search( Plugin_API ):

    def trigger( self ):

        # Google search
        if self.command("google") or self.command("g"):
            lang = "en"     # remember to change your language if needed!
            args    = self.args()
            search = urllib.quote( " ".join(args) )
            link = "http://google.com/search?q=%s&hl=%s" % (search, lang)
            self.irc.msg(self.reply, link)
            return

        # YouTube search
        if self.command("youtube") or self.command("tube"):
            args    = self.args()
            search = urllib.quote( " ".join(args) )
            link = "http://youtube.com/results?search_query=%s" % ( search )
            self.irc.msg(self.reply, link)
            return

        # PirateBay (For Linux Distros)
        if self.command("tpb") or self.command("pirate"):
            args    = self.args()
            search = urllib.quote( " ".join(args) )
            link = "http://thepiratebay.se/search/%s/0/7/0" % ( search )
            self.irc.msg(self.reply, link)
            return

        # Grooveshark
        if self.command("grooveshark") or self.command("groove"):
            args    = self.args()
            search = urllib.quote( " ".join(args) )
            link = "http://grooveshark.com/#!/search?q=%s" % ( search )
            self.irc.msg(self.reply, link)
            return

