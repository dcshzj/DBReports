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

import DBRCore

class DBRblankiptalk:
	def __init__( self, db='' ):
		self.dbquery = DBRCore.DBQuery( db )
		self.Wiki = DBRCore.Wiki( db )
		self.database = db

	def execute( self ):
		title = "Blank user talk pages for IPs"
		query = "SELECT ns_name, page_title FROM page JOIN s51892_toolserverdb_p.namespace ON ns_id = page_namespace WHERE dbname = %s AND page_namespace = 3 AND page_title RLIKE %s AND page_len = 0 LIMIT 1000;", ( self.database, r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$' )
 		template = '''Blank user talk pages of anonymous users (limited to the first 1000 entries); data as of <onlyinclude>%s</onlyinclude>.

{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! No.
! Page
|-
%s
|}

[[Category:{{subst:SITENAME}} database reports|{{SUBPAGENAME}}]]
'''
		rows = self.dbquery.execute( query )
		i = 1
		output = []
		for row in rows:
			nsname = u'%s' % unicode( row[0], 'utf-8' )
			pagetitle = u'%s' % unicode( row[1], 'utf-8' )
			fullpagetitle = u'[[%s:%s|%s]]' % ( nsname, pagetitle, pagetitle )
			tablerow = u'| %d\n| %s\n|-' % ( i, fullpagetitle )
			output.append( tablerow )
			i += 1
		contents = template % ( self.Wiki.getDataAsOf(), '\n'.join( output ) )
		self.Wiki.outputToWiki( title, contents )

if __name__ == "__main__":
	print "This module should not be called directly! Please use dbr.py to run the database reports."