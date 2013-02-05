from random import randrange
from api import *

# Russian Roulette, six-shooter

class Roulette_Game:

    def __init__( self ):
        self.num_rounds = 6
        self.restart()

    def restart( self ):
        self.current = 1
        self.bullet = randrange(self.num_rounds) + 1

    def hit( self ):

        if self.current == self.bullet:
            self.restart()
            return 1
        else:
            self.current += 1
            return 0


class Roulette( Plugin_API ):

    def launcher( self ):
        self.games = {}

    def trigger( self ):

        if ( self.command("roulette") or self.command("r") ):

            self.add_game(self.reply)    # make sure game exists

            if self.games[self.reply].hit():
                self.irc.msg( self.reply, ( "%s: BANG!" % self.sender ) )
            else:
                self.irc.msg( self.reply, "*click*" )


    # add new game if needed
    def add_game( self, name ):

        try:
            self.games[name]
        except KeyError:
            self.games[name] = Roulette_Game()


