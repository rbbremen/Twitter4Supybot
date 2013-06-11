 _______       _ _   _              _  _   
|__   __|     (_) | | |            | || |  
   | |_      ___| |_| |_ ___ _ __  | || |_ 
   | \ \ /\ / / | __| __/ _ \ '__| |__   _|
   | |\ V  V /| | |_| ||  __/ |       | |  
   |_| \_/\_/ |_|\__|\__\___|_|       |_| 
  _____                   _           _   
 / ____|                 | |         | |  
| (___  _   _ _ __  _   _| |__   ___ | |_ 
 \___ \| | | | '_ \| | | | '_ \ / _ \| __|
 ____) | |_| | |_) | |_| | |_) | (_) | |_ 
|_____/ \__,_| .__/ \__, |_.__/ \___/ \__|
             | |     __/ |                
             |_|    |___/                 

Welcome to twitter4supybot, a plugin for Supybot
https://sourceforge.net/projects/supybot/
Thanx to James Vega and Jeremy Fincher for this
Swiss knife IRC bot!

last version of this plugin is available at
https://sourceforge.net/projects/rbbremen.u/files/
https://github.com/rbbremen/Twitter4Supybot


Requirements:

  - Python 2.5 or newer, running on Linux 
    with the following modules:

      Python Lib 'phython-irclib-0.4.8'
      http://pypi.python.org/pypi/python-irclib/

      Python Lib 'twitter-1.4.2.tar.gz'
      http://pypi.python.org/pypi/twitter/
 
      Python Lib MySQLdb or psycopg2 if you want 
      a database backend
      http://pypi.python.org/pypi/MySQL-python/
      http://pypi.python.org/pypi/psycopg2/

  - and of course a running Supybot on IRC channel
  

Installation:

Install all needed Python libraries. Register the Python-Twitter-lib
at Twitter.com to be able to connect via ".twitter_oauth".
Read the documentation in the Python-Twitter-lib!

Copy the directory Twitter from archive into desired plugin-directory.
Loading the plugin Twitter with Supybot-Cmd 'load Twitter' should
be possible.

Configuration:
Supybot-Cmd 'search Twitter' shows all configurable variables.
Supybot-Cmd 'config supybot.plugins.Twitter.command' should return 
pathname of cmdline-tool. Example '/usr/bin/twitter'.

Usage:
After loading plugin you can use the commands twfriends, twglobal, 
twreplies. The output appears in the channel or query from where
command was executed. Use the Scheduler plugin for automation.

The estimated number of rows, in dependency of time between two calls,
has to be a lower value as configured as default. Else you will loose
rows if you do not poll the next lines fast enough. I follow only 100
feeds with low traffic so 20 lines in twitter-lib and a call every 60
seconds works fine for me.
Supybot-Cmd 'scheduler repeat twf 60 twfriends'

A proper documentation for Supybot is called Supybook.
You cand find it here -> http://supybook.fealdia.org/
Thanx to Heikki Hokkanen for this great job!
        
Have fun!


HISTORY
----------------------------------------------------------------------
2011-10-03 v0.22: Propper escaped SQL string handling.
                  Enabled autocommit for psycopg (PostgreSQL).

2011-10-02 v0.21: Added PostgreSQL database interface

2011-10-01 v0.20: Added MySQL database interface

2011-06-17 v0.10: Initial release

