# Copyright (C) 2015 Hydriz Scholz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA, or visit
# <http://www.gnu.org/copyleft/gpl.html>

import reports
import settings
import DBRCore
import sys
import urllib2

class DBR:
	def __init__( self, wikidb ):
		self.database = wikidb
		if ( self.database == "simplewiki" ):
			self.statuspage = "https://simple.wikipedia.org/w/index.php?title=User:%s/%s&action=raw" % ( settings.username, settings.controlpage )
		elif ( self.database == "simplewiktionary" ):
			self.statuspage = "https://simple.wiktionary.org/w/index.php?title=User:%s/%s&action=raw" % ( settings.username, settings.controlpage )

	def getBotStatus( self, function ):
		headers = { 'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)' }
		statuspage = urllib2.urlopen( urllib2.Request( self.statuspage, headers=headers ) )
		status = 'disabled' # Default, especially when the page has been vandalised
		for line in statuspage:
			prefix = "%s: " % ( function )
			if ( line.startswith( prefix ) ):
				status = line.replace( prefix, '' )
				break
			else:
				continue
		if ( status == 'enabled\n' ):
			status = 'enabled'
		else:
			status = 'disabled'
		return status

	def run( self, function ):
		status = self.getBotStatus( function )
		if ( status == 'enabled' ):
			report = getattr( reports, 'DBR%s' % ( function ) )( self.database )
			report.execute()
		else:
			# This function has been disabled on-wiki, or someone has vandalised it
			# Nonetheless, we are going to disable it just in case
			print "ERROR: The bot function \"%s\" has been forcefully disabled on-wiki" % ( function )

if __name__ == "__main__":
	DBR = DBR( sys.argv[1] )
	DBR.run( sys.argv[2] )