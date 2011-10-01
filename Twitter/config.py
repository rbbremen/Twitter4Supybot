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

import supybot.conf as conf
import supybot.utils as utils
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Twitter', True)

Twitter = conf.registerPlugin('Twitter')

conf.registerGlobalValue(Twitter, 'command',
    registry.String(utils.findBinaryInPath('twitter') or '', """Determines
    what command will be called for the twitter command."""))

conf.registerGlobalValue(Twitter, 'optionsF',
    registry.String(' -t -d', """Determines what
    options will be used for the twitter command friends."""))

conf.registerGlobalValue(Twitter, 'optionsG',
    registry.String('on_pvt_ircd_only -t -d', """Determines what
    options will be used for the twitter command global."""))

conf.registerGlobalValue(Twitter, 'optionsR',
    registry.String('replies -t -d', """Determines what
    options will be used for the twitter command replies."""))

conf.registerGlobalValue(Twitter, 'UseRDB',
    registry.Boolean(False, """Determines whether database management
    is active or not.""")) 

conf.registerGlobalValue(Twitter, 'RDBsql',
    registry.String('postgresql', """Determines the used
    database server for storing information and received
    tweets etc. Possible values are 'mysql' and 'postgresql'."""))

conf.registerGlobalValue(Twitter, 'RDBhost',
    registry.String('localhost', """Determines the domainname or ipaddr
    of the database server. default: localhost"""))

conf.registerGlobalValue(Twitter, 'RDBport',
    registry.String('5432', """Determines the port for the
    database server. default ports: mysql 3306, postgresql 5432"""))

conf.registerGlobalValue(Twitter, 'RDBdb',
    registry.String('Twitter', """Determines the name of the
    database used on server."""))

conf.registerGlobalValue(Twitter, 'RDBuser',
    registry.String('fanboy', """Determines the name
    of the useraccount on database server."""))

conf.registerGlobalValue(Twitter, 'RDBpass',
    registry.String('secret', """Determines the used
    password for account on the database server."""))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
