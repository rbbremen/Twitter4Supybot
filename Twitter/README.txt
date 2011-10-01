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
#  _______       _ _   _              _  _   
# |__   __|     (_) | | |            | || |  
#    | |_      ___| |_| |_ ___ _ __  | || |_ 
#    | \ \ /\ / / | __| __/ _ \ '__| |__   _|
#    | |\ V  V /| | |_| ||  __/ |       | |  
#    |_| \_/\_/ |_|\__|\__\___|_|       |_| 
#   _____                   _           _   
#  / ____|                 | |         | |  
# | (___  _   _ _ __  _   _| |__   ___ | |_ 
#  \___ \| | | | '_ \| | | | '_ \ / _ \| __|
#  ____) | |_| | |_) | |_| | |_) | (_) | |_ 
# |_____/ \__,_| .__/ \__, |_.__/ \___/ \__|
#              | |     __/ |                
#              |_|    |___/                 
#

Requirements:
 - installed Supybot
 - Python Lib 'phython-irclib-0.4.8'
 - Python Lib 'twitter-1.4.2.tar.gz'
 - Python Lib MySQLdb or psycopg2
 - Python 2.5 or newer

twitter-1.4.2-py2.5.egg -> http://pypi.python.org/pypi/twitter/1.4.2

Installation:
Copy the directory Twitter from archive into desired plugin-directory.
Loading the plugin Twitter with Supybot-Cmd 'load Twitter' should
be possible.

Configuration:
Supybot-Cmd 'search Twitter' shows all configurable variables.
Supybot-Cmd 'config supybot.plugins.Twitter.command' should return 
pathname of cmdline-tool. Example '/usr/bin/twitter'.

Usage:
After loading plugin you can use the commands twfriends, twglobal, 
twreplies and twversion. The output appears in the channel or query
from where command was executed. Use the Scheduler plugin for automation.

The estimated number of rows, in dependency of time between two calls,
has to be a lower value as configured as default. Else you will loose
rows if you don´t poll the next lines fast enough. I follow only 100
feeds with low traffic so 20 lines in twitter-lib and a call every 60
seconds works fine for me.
Supybot-Cmd 'scheduler repeat twf 60 twfriends'
        
Have fun!


HISTORY

2011-06-17 Version 0.10: initial release
2011-10-01 Vserion 0.20: added database interface

