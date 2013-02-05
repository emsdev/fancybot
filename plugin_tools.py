from random import randrange
import string
import hashlib
import time
from api import *


class Tools( Plugin_API ):

    def trigger( self ):

        # Dice - rand(1,6) ###
        if self.command("dice"):
            dice = randrange(5) + 1
            self.irc.msg(self.reply, dice)
            return

        # md5 ###
        if self.command("md5"):
            args    = self.args()
            hasher  = hashlib.md5()
            hasher.update( " ".join(args) )
            md5hash = hasher.hexdigest()
            self.irc.msg(self.reply, md5hash)
            return

        # unix timestamp
        if self.command("unixtime") or self.command("utime"):
            self.irc.msg(self.reply, int( time.time() ) )
            return
