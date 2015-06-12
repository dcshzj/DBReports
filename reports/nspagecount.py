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

class DBRnspagecount:
	def __init__( self, db='' ):
		self.dbquery = DBRCore.DBQuery( db )
		self.Wiki = DBRCore.Wiki( db )

	def execute( self ):
		title = "Page count by namespace"
		template = '''The number of pages in each [[{{subst:SITENAME}}:Namespace|namespace]]; data as of <onlyinclude>%s</onlyinclude>.

{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! [[{{subst:SITENAME}}:Namespace|ID]]
! Name
! Non-redirects
! Redirects
! Total
|-
%s
|- class="sortbottom"
! colspan="2" | Totals
! style="text-align:left;" | %s
! style="text-align:left;" | %s
! style="text-align:left;" | %s
|}

[[Category:{{subst:SITENAME}} database reports|{{SUBPAGENAME}}]]
'''
		output = []
		for ns in self.namespaces:
			noredirectsquery = "SELECT COUNT(*) FROM page WHERE page_namespace='%d' AND page_is_redirect='0';" % ( ns )
			redirectsquery = "SELECT COUNT(*) FROM page WHERE page_namespace='%d' AND page_is_redirect='1';" % ( ns )
			totalquery = "SELECT COUNT(*) FROM page WHERE page_namespace='%d';" % ( ns )
			noredirects = self.dbquery.execute( noredirectsquery )
			for noredirect in noredirects:
				nordr = noredirect[0]
			redirects = self.dbquery.execute( redirectsquery )
			for redirect in redirects:
				rdr = redirect[0]
			total = self.dbquery.execute( totalquery )
			for summ in total:
				tot = summ[0]
			tablerow = "| %d\n| {{subst:ns:%d}}\n| %s\n| %s\n| %s\n|-" % ( ns, ns, nordr, rdr, tot )
			output.append( tablerow )
		totalnoredirectsquery = "SELECT COUNT(*) FROM page WHERE page_is_redirect='0';"
		totalredirectsquery = "SELECT COUNT(*) FROM page WHERE page_is_redirect='1';"
		grandtotalquery = "SELECT COUNT(*) FROM page;"
		totalnoredirects = self.dbquery.execute( totalnoredirectsquery )
		for totalnoredirect in totalnoredirects:
			totnordr = totalnoredirect[0]
		totalredirects = self.dbquery.execute( totalredirectsquery )
		for totalredirect in totalredirects:
			totrdr = totalredirect[0]
		grandtotal = self.dbquery.execute( grandtotalquery )
		for grand in grandtotal:
			grant = grand[0]
		contents = template % ( self.Wiki.getDataAsOf(), '\n'.join( output ), totnordr, totrdr, grant )
		self.Wiki.outputToWiki( title, contents )

if __name__ == "__main__":
	print "This module should not be called directly! Please use dbr.py to run the database reports."