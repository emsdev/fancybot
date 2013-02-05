#! /usr/bin/python2

##############################################################################
#
#  fancyBot - Simple IRC Bot written in Python
#  Version: 0.1.2
#
#  Author:  ems <ems@lavabit.com>
#  License: GPLv2
#
#  WWW:     https://github.com/emsdev/fancybot
#
##############################################################################

import os
import sys
import socket
import string
import time


# Create IRC connection socket, listen, send, basic IRC commands, etc.
##############################################################################

class IRC_Connection:

    # connect to IRC server
    def __init__( self, config ):

        self.connection = socket.socket( )
        self.connection.connect( (config['server'], config['port']) )
        self.nick(config['nick']) # set default nick

        self.connection.send( "USER %s %s %s :%s\r\n" % ( config['ident'],
                              config['hostname'], config['server'],
                              config['realname'] ) )

    # Basic input and output ################################

    # Send "raw" line to IRC server
    def send( self, line ):
        self.connection.send( line + "\r" + "\n" )

    # Return list of new lines sent by IRC server
    def read( self ):
        data = self.connection.recv( 4096 )
        lines = string.split( data, "\n" )
        return lines

    # Basic IRC commands ####################################

    # Set/change nick
    def nick( self, nick ):
        self.send( "NICK %s" % nick )

    # Join new channel
    def join(self, channel):
        self.send( "JOIN :%s" % channel )

    # Part channel
    def part(self, channel):
        self.send( "PART :%s" % channel )

    # Send message to channel/nick
    def msg(self, target, message):
        self.send( "PRIVMSG %s :%s" % ( target, message ) )



class Plugin_Container:

    def __init__( self, irc_connection, config ):
        self.plugins = [] # here we store plugins
        self.irc = irc_connection
        self.config = config

    def module_import(self, name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    # load new plugin
    def load( self, plugin_name ):

        # import module
        module = self.module_import("plugin_" + plugin_name)
        plugin_class_name = plugin_name[0].upper() + plugin_name[1:]

        new_plugin = eval("module."+plugin_class_name)(self.irc, self.config)
        new_plugin.launcher()

        self.plugins.append( new_plugin )

    # Execute all plugin triggers
    def run(self, sender, target, message, msgtype):
        for plugin in self.plugins:
            plugin.trigger_prepare(sender, target, message, msgtype)
            plugin.trigger()



# Config, startup and ticker
##############################################################################

class Fancy_Bot:

    def __init__( self ):

        # Config                                     *** REMEMBER TO EDIT! ***
        self.config = {
            'network'        : 'Freenode',
            'server'         : 'chat.freenode.net',
            'port'           : 6667,
            'ident'          : 'bot',               # *nix username
            'hostname'       : 'auto',
            'nick'           : 'fancybot1234',
            'realname'       : 'bot',

            'adminpw'        : 'pass123',
            'cmdprefix'      : '.',
            'channels'       : ['#fancybot1234'],   # list of channels
            'plugins'        : ['calculator', 'roulette', 'search', 'tools'] # list of enabled plugins
        }

        # Do not edit!
        self.nick = self.config['nick']
        self.channels = []

        # Connect to IRC server and join to all channels
        self.irc = IRC_Connection( self.config )
        for chan in self.config['channels']:
            self.irc.join( chan )

        # Load plugins
        self.plugins = Plugin_Container(self.irc, self.config)

        for plugin in self.config['plugins']:
            self.plugins.load( plugin )

        # Launch event ticker
        self.ticker()

    # Runs continuously and listens and acts on events
    def ticker( self ):

        while True:
            lines = self.irc.read() # get new line(s)

            for line in lines:
                line = line.rstrip( "\r\n" )
                print line # DEBUG

                # Reply to ping
                if line[0:4] == "PING":
                    self.irc.send( "PONG %s" % ( line[5:] ) )
                    continue

                # explode line into pieces
                if line[0:1] == ":":

                    parts = string.split(line, " ")

                    if len( parts ) >= 4:

                        if parts[1] == "433": # nickname in use
                            self.nick += "_"
                            self.irc.nick(self.nick)


                        # Detect channel/private messages #############

                        elif parts[1] == "PRIVMSG":

                            sender = parts[0][ 1 : parts[0].find("!") ]

                            target = parts[2]
                            message = " ".join(parts[3:])
                            message = message[1:]         # remove heading ':'
                            #message = message.rstrip( "\r\n" )


                            msg_parts = string.split(message, " ")

                            if target == self.nick:
                                msgtype = "private"
                            else:
                                msgtype = "public"


                            # run all plugin operations
                            self.plugins.run(sender, target, message, msgtype)


# Let's launch the Bot!
Fancy_Bot()

