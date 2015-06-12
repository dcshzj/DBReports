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

import datetime
import MySQLdb
import settings
import wikitools

class DBQuery:
	def __init__( self, database='', host='s3.labsdb', read_default_file='~/.my.cnf' ):
		self.read_default_file = read_default_file
		self.host = host
		self.database = database + '_p'

	def execute( self, query ):
		conn = MySQLdb.connect( host=self.host, db=self.database, read_default_file=self.read_default_file )
		cursor = conn.cursor()
		cursor.execute( query )
		result = cursor.fetchall()
		cursor.close()
		conn.close()
		return result

class Wiki:
	def __init__( self, wikidb ):
		self.database = wikidb
		if ( self.database == "simplewiki" ):
			self.apiUrl = "https://simple.wikipedia.org/w/api.php"
			self.reportPrefix = "Wikipedia:Database reports"
		elif ( self.database == "simplewiktionary" ):
			self.apiUrl = "https://simple.wiktionary.org/w/api.php"
			self.reportPrefix = "Wiktionary:Database reports"
		self.username = settings.username
		self.password = settings.password
		self.summary = settings.summary

	def outputToWiki( self, title, contents ):
		self.wiki = wikitools.Wiki( self.apiUrl )
		self.wiki.login( self.username, self.password )
		title = "%s/%s" % ( self.reportPrefix, title )
		report = wikitools.Page( self.wiki, title )
		reporttext = contents
		report.edit( reporttext, summary=self.summary, bot=1 )

	def getDataAsOf( self ):
		query = "SELECT UNIX_TIMESTAMP() - UNIX_TIMESTAMP(rc_timestamp) FROM recentchanges ORDER BY rc_timestamp DESC LIMIT 1;"
		self.DBQuery = DBQuery( self.database )
		replag = self.DBQuery.execute( query )
		for seconds in replag:
			result = ( datetime.datetime.utcnow() - datetime.timedelta( seconds=int( float( seconds[0] ) ) ) ).strftime( '%H:%M, %d %B %Y (UTC)' )
		return result

if __name__ == "__main__":
	print "This module should not be called directly! Please use dbr.py to run the database reports."