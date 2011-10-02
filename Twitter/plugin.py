# -*- coding: utf-8 -*-
#
# Twitter4Supybot - A plugin to access services at twitter.com
# Copyright (C) 2011 Robert Bergermann (rbergermann at googlemail dot com)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation; either version 2 
# of the License, or (at your option) any later version. 
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details. 
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
# MA 02110, USA 
#
###

import os
import subprocess
from datetime import date
import supybot.conf as conf
import supybot.utils as utils
import supybot.world as world
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks



def pgsqlinsert(curs, msg):
    curs.execute("""INSERT INTO tblTwitter (twitt) VALUES (%s)""", (msg,))


def mysqlinsert(conn, msg):
    curs = conn.cursor()
    curs.execute("""INSERT INTO tblTwitter (twitt) VALUES (%s)""", (msg,))


class CdbTwitterDB(object):
    def __init__(self, filename):
        self.dbs = {}
        cdb = conf.supybot.databases.types.cdb
        for service in ['friends','global','replies']:
            dbname = filename.replace('.db', service.capitalize() + '.db')
            self.dbs[service] = cdb.connect(dbname)

    def get(self, service, twitt):
        return self.dbs[service][twitt]

    def set(self, service, twitt, twittID):
        self.dbs[service][twitt] = twittID

    def close(self):
        for service in self.dbs:
            self.dbs[service].close()

    def flush(self):
        for service in self.dbs:
            self.dbs[service].flush()

TwitterDB = plugins.DB('Twitter', {'cdb': CdbTwitterDB})


class Twitter(callbacks.Plugin):
    """This plugin is for accessing a Twitter account"""
    threaded = False
    rdbActive = False
    rdbSql = ""
    conn = ""
    curs = ""

    def __init__(self, irc):
        self.__parent = super(Twitter, self)
        self.__parent.__init__(irc)
        self.lastRequest = ""
        self.db = TwitterDB()
        self.rdbActive = self.registryValue('rdbActive')
        if self.rdbActive == True:
            self.rdbSql  = self.registryValue('rdbSql')
            rdbHost = self.registryValue('rdbHost')
            rdbPort = self.registryValue('rdbPort')
            rdbName   = self.registryValue('rdbName')
            rdbUser = self.registryValue('rdbUser')
            rdbPassword = self.registryValue('rdbPassword')
            if self.rdbSql == 'mysql':
                import MySQLdb
                self.conn = MySQLdb.connect(rdbHost, rdbUser, \
                    rdbPassword, rdbName, int(rdbPort))
            else:
                import psycopg2
                import psycopg2.extensions
                DSN = 'dbname=%s user=%s password=%s host=%s port=%s' \
                % (rdbName, rdbUser, rdbPassword, rdbHost, rdbPort)
                self.conn = psycopg2.connect(DSN)
                self.conn.set_isolation_level( \
                    psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                self.curs = self.conn.cursor()

    def die(self):
        self.db.close()
        if self.rdbActive == True:
            self.conn.close()

    def __call__(self, irc, msg):
        self.__parent.__call__(irc, msg)
        irc = callbacks.SimpleProxy(irc, msg)


    def twfriends(self, irc, msg, args):
        """takes no arguments
        call cmdline-tool and return a status lines from Twitter->friends
        """
        cmdTwitter =  self.registryValue('command')
        cmdTwitter += ' ' + self.registryValue('optionsF')
        self.log.debug('twfriends: cmdline %s', cmdTwitter)
        if cmdTwitter:
            args = [cmdTwitter]
            try:
                inst = subprocess.Popen(args, close_fds=True,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=file(os.devnull))
            except OSError, e:
                irc.error('It seems the configured twitter command was '
                          'not available.', Raise=True)
            (out, err) = inst.communicate()
            inst.wait()
            lines = out.splitlines()
            lines = map(str.rstrip, lines)
            lines = filter(None, lines)
            neues = []
            for x in lines:
                # for each line in lines, first try to get the last if exists
                try:
                    last = neues.pop()
                except IndexError:
                    last = ""
                # check timestamp at linestart, append to last if none
                now = date.today()
                if x.startswith(now.strftime('%Y')):
                    if len(last)>0:
                        neues.append(last)
                    neues.append(x)
                else:
                    if len(last)>0:
                        last += ' ' + x
                        neues.append(last)
                    else:
                        irc.error('No Last and no Timestamp-Error', Raise=True)

            # Now store new lines in db to avoid posting dupes
            for x in neues:
                try:
                    twID = self.db.get('friends', x)
                except KeyError:
                    self.db.set( 'friends', x, x[5:25] )
                    irc.reply(x)
                    if self.rdbActive == True:
                        if self.rdbSql == 'postgres':
                            pgsqlinsert(self.curs, x)
                        else:
                            mysqlinsert(self.conn, x)

        else:
            irc.error('The Twitter.twfriends command is not configured. If is '
                      'installed, reconfigure the '
                      'supybot.plugins.Twitter.command and optionsF '
                      'variable appropriately.')



    def twglobal(self, irc, msg, args):
        """takes no arguments
        call cmdline-tool and return a status line from Twitter->global
        """
        cmdTwitter =  self.registryValue('command')
        cmdTwitter += ' ' + self.registryValue('optionsG')
        self.log.debug('twglobal: cmdline %s', cmdTwitter)
        if cmdTwitter:
            args = [cmdTwitter]
            try:
                inst = subprocess.Popen(args, close_fds=True,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=file(os.devnull))
            except OSError, e:
                irc.error('It seems the configured twitter command was '
                          'not available.', Raise=True)
            (out, err) = inst.communicate()
            inst.wait()
            lines = out.splitlines()
            lines = map(str.rstrip, lines)
            lines = filter(None, lines)
            neues = []
            for x in lines:
                # for each line in lines, first try to get the last if exists
                try:
                    last = neues.pop()
                except IndexError:
                    last = ""
                # check timestamp at linestart, append to last if none
                now = date.today()
                if x.startswith(now.strftime('%Y')):
                    if len(last)>0:
                        neues.append(last)
                    neues.append(x)
                else:
                    if len(last)>0:
                        last += ' ' + x
                        neues.append(last)
                    else:
                        irc.error('No Last and no Timestamp-Error', Raise=True)
            # Now store new lines in db to avoid posting dupes
            for x in neues:
                try:
                    twID = self.db.get('global', x)
                except KeyError:
                    self.db.set( 'friends', x, x[5:25] )
                    irc.reply(x)
        else:
            irc.error('The Twitter.twglobal command is not configured. If is '
                      'installed, reconfigure the '
                      'supybot.plugins.Twitter.command and optionsG '
                      'variable appropriately.')



    def twreplies(self, irc, msg, args):
        """takes no arguments
        call cmdline-tool and return a status lines from Twitter->replies
        """
        cmdTwitter =  self.registryValue('command')
        cmdTwitter += ' ' + self.registryValue('optionsR')
        self.log.debug('twreplies: cmdline %s', cmdTwitter)
        if cmdTwitter:
            args = [cmdTwitter]
            try:
                inst = subprocess.Popen(args, close_fds=True,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=file(os.devnull))
            except OSError, e:
                irc.error('It seems the configured twitter command was '
                          'not available.', Raise=True)
            (out, err) = inst.communicate()
            inst.wait()
            lines = out.splitlines()
            lines = map(str.rstrip, lines)
            lines = filter(None, lines)
            neues = []
            for x in lines:
                # for each line in lines, first try to get the last if exists
                try:
                    last = neues.pop()
                except IndexError:
                    last = ""
                # check timestamp at linestart, append to last if none
                now = date.today()
                if x.startswith(now.strftime('%Y')):
                    if len(last)>0:
                        neues.append(last)
                    neues.append(x)
                else:
                    if len(last)>0:
                        last += ' ' + x
                        neues.append(last)
                    else:
                        irc.error('No Last and no Timestamp-Error', Raise=True)
            # Now store new lines in db to avoid posting dupes
            for x in neues:
                try:
                    twID = self.db.get('replies', x)
                except KeyError:
                    self.db.set( 'friends', x, x[5:25] )
                    irc.reply(x)
        else:
            irc.error('The Twitter.twreplies command is not configured. If is '
                      'installed, reconfigure the '
                      'supybot.plugins.Twitter.command and optionsR '
                      'variable appropriately.')

Class = Twitter


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
