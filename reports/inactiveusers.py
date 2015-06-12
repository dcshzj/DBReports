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

class DBRinactiveusers:
	def __init__( self, db='' ):
		self.dbquery = DBRCore.DBQuery( db )
		self.Wiki = DBRCore.Wiki( db )

	def execute( self ):
		title = "Inactive users in user groups"
		query = "SELECT DISTINCT user_name, rev_timestamp, GROUP_CONCAT(ug_group) FROM user JOIN user_groups ON ug_user = user_id JOIN revision ON rev_user = user_id WHERE user_name NOT IN (SELECT user_name FROM user JOIN user_groups ON ug_user = user_id WHERE ug_group IN ('rollbacker')) AND (SELECT MAX(rev_timestamp) FROM revision WHERE rev_user = user_id) < DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 1 YEAR),'%Y%m%d%H%i%s') AND rev_timestamp = (SELECT MAX(rev_timestamp) FROM revision WHERE rev_user = user_id) GROUP BY user_name;"
		template = '''Users in user groups without any contributions in the past one year (Rollbackers are excluded); data as of <onlyinclude>%s</onlyinclude>.

{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! No.
! User
! Last edit
! User groups
|-
%s
|}

[[Category:{{subst:SITENAME}} database reports|{{SUBPAGENAME}}]]
'''
		rows = self.dbquery.execute( query )
		i = 1
		output = []
		for row in rows:
			username = '[[User:%s|]]' % ( row[0] )
			revtimestamp = '[[Special:Contributions/%s|%s]]' % ( row[0], row[1] )
			usergroups = '%s' % ( row[2] )
			tablerow = '| %d\n| %s\n| %s\n| %s\n|-' % ( i, username, revtimestamp, usergroups )
			output.append( tablerow )
			i += 1
		contents = template % ( self.Wiki.getDataAsOf(), '\n'.join( output ) )
		self.Wiki.outputToWiki( title, contents )

if __name__ == "__main__":
	print "This module should not be called directly! Please use dbr.py to run the database reports."