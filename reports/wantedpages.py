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

class DBRwantedpages:
	def __init__( self, db='' ):
		self.dbquery = DBRCore.DBQuery( db )
		self.Wiki = DBRCore.Wiki( db )

	def execute( self ):
		title = "Wanted pages"
		template = '''List of most wanted pages on the wiki (limited to 500 results). This data is current as of <onlyinclude>%s</onlyinclude>.

{| class="wikitable sortable" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! No.
! [[{{subst:SITENAME}}:Namespace|ID]]
! Page
! Links
|-
%s
|}

[[Category:{{subst:SITENAME}} database reports|{{SUBPAGENAME}}]]
'''
		query = "SELECT pl_namespace, pl_title, COUNT(*) AS nlinks FROM pagelinks LEFT JOIN page pg1 ON pl_namespace = pg1.page_namespace AND pl_title = pg1.page_title LEFT JOIN page pg2 ON pl_from = pg2.page_id WHERE pg1.page_namespace IS NULL AND pl_namespace NOT IN ( 2, 3 ) AND pg2.page_namespace != 8 GROUP BY pl_namespace, pl_title ORDER BY nlinks DESC LIMIT 500;"
		rows = self.dbquery.execute( query )
		i = 1
		output = []
		for row in rows:
			nsid = row[0]
			pagetitle = '%s' % unicode( row[1], 'utf-8' )
			if ( nsid == 6 or nsid == 14 ):
				pagetitle = ':{{subst:ns:%s}}:%s' % ( nsid, pagetitle )
			elif ( nsid == 0 ):
				pagetitle = '%s' % ( pagetitle )
			else:
				pagetitle = '{{subst:ns:%s}}:%s' % ( nsid, pagetitle )
			links = row[2]
			tablerow = '| %d\n| %s\n| {{autostrike|%s}}\n| %s\n|-' % ( i, nsid, pagetitle, links )
			output.append( tablerow )
			i += 1
		contents = template % ( self.Wiki.getDataAsOf(), '\n'.join( output ) )
		self.Wiki.outputToWiki( title, contents )

if __name__ == "__main__":
	print "This module should not be called directly! Please use dbr.py to run the database reports."