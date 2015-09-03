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

class DBRtemplatedata:
	def __init__( self, db='' ):
		self.dbquery = DBRCore.DBQuery( db )
		self.Wiki = DBRCore.Wiki( db )

	def execute( self ):
		title = "Templates without TemplateData"
		template = '''Templates without [[{{subst:SITENAME}}:TemplateData|TemplateData]] documentation in them; data as of <onlyinclude>%s</onlyinclude>.

{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! No.
! Template
|-
%s
|}

[[Category:{{subst:SITENAME}} database reports|{{SUBPAGENAME}}]]
'''
		query = "SELECT page_title FROM page LEFT JOIN page_props ON page_id=pp_page WHERE pp_propname='templatedata' AND page_namespace='10';"
		withtemplatedata = self.dbquery.execute( query )
		templates = "SELECT page_title FROM page WHERE page_namespace='10' AND page_is_redirect='0' ORDER BY page_title;"
		results = self.dbquery.execute( templates )
		i = 1
		output = []
		for result in results:
			if ( result in withtemplatedata ):
				continue
			else:
				tablerow = "| %d\n| [[Template:%s]]\n|-" % ( i, result[0].decode( 'utf8' ) )
				output.append( tablerow )
				i += 1
		contents = template % ( self.Wiki.getDataAsOf(), '\n'.join( output ) )
		self.Wiki.outputToWiki( title, contents.encode( 'utf8' ) )

if __name__ == "__main__":
	print "This module should not be called directly! Please use dbr.py to run the database reports."