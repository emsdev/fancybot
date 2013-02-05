# Plugin API

import string

class Plugin_API:

    def __init__(self, irc_connection, config ):

        self.irc = irc_connection   # irc connection
        self.config = config        # see 'bot.py' for content

    def trigger_prepare(self, sender, target, message, msgtype):

        self.sender = sender        # message's sender
        self.target = target        # channel or bot's nick
        self.message = message      # message's content
        self.msgtype = msgtype      # 'private' or 'public'

        if self.msgtype == "public":
            self.reply = target
        else:
            self.reply = sender


    # check if message starts with given command name
    def command( self, cmd_name ):

        message_parts = string.split(self.message, " ")

        if len( message_parts ) >= 1:
            if message_parts[0][0:1] == self.config['cmdprefix']:
                if message_parts[0][1:] == cmd_name:

                    return True

        return False


    # return list of command arguments
    def args(self):

        message_parts = string.split(self.message, " ")

        if len( message_parts ) > 0:
            message_parts.pop(0)

        return message_parts


    # defaults ############################################

    def launcher(self):
        return          # do nothing by default

    def trigger(self):
        return          # do nothing by default


