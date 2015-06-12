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

class DBRuserprefs:
	def __init__( self, db='' ):
		self.dbquery = DBRCore.DBQuery( db )
		self.Wiki = DBRCore.Wiki( db )

	def execute( self ):
		title = "User preferences"
		template = '''User preferences statistics; data as of <onlyinclude>%s</onlyinclude>.

== Gender ==
{| class="wikitable sortable plainlinks" style="width:80%%;"
|- style="white-space:nowrap;"
! Gender
! Users
|-
%s
|}

== Language ==
{| class="wikitable sortable plainlinks" style="width:80%%;"
|- style="white-space:nowrap;"
! Language code
! Language name
! Users
|-
%s
|}

== Skin ==
{| class="wikitable sortable plainlinks" style="width:80%%;"
|- style="white-space:nowrap;"
! Skin
! Users
|-
%s
|}

== Gadgets ==
{| class="wikitable sortable plainlinks" style="width:80%%;"
|- style="white-space:nowrap;"
! Gadget
! Users
|-
%s
|}

[[Category:{{subst:SITENAME}} database reports|{{SUBPAGENAME}}]]
'''
		genderquery = "SELECT up_value, COUNT(*) FROM user_properties WHERE up_property = 'gender' GROUP BY up_value;"
		languagequery = "SELECT up_value, COUNT(*) FROM user_properties WHERE up_property = 'language' GROUP BY up_value;"
		skinquery = "SELECT up_value, COUNT(*) FROM user_properties WHERE up_property = 'skin' GROUP BY up_value;"
		gadgetsquery = "SELECT up_property, COUNT(*) FROM user_properties_anon WHERE up_property LIKE 'gadget-%' AND up_value = 1 GROUP BY up_property;"
		gender = self.dbquery.execute( genderquery )
		gender_output = []
		for genderrow in gender:
			up_value = '{{MediaWiki:gender-%s}}' % genderrow[0]
			count = genderrow[1]
			table_row = '''\
| %s
| %s
|-''' % (up_value, count)
			gender_output.append(table_row)
		language = self.dbquery.execute( languagequery )
		language_output = []
		for languagerow in language:
			lang_code = languagerow[0]
			lang_name = '{{#language:%s}}' % languagerow[0]
			count = languagerow[1]
			table_row = u'''\
| %s
| %s
| %s
|-''' % (lang_code, lang_name, count)
			language_output.append(table_row)
		skin = self.dbquery.execute( skinquery )
		skin_output = []
		for skinrow in skin:
			up_value = '{{MediaWiki:skinname-%s}}' % skinrow[0]
			count = skinrow[1]
			table_row = u'''\
| %s
| %s
|-''' % (up_value, count)
			skin_output.append(table_row)
		gadgets = self.dbquery.execute( gadgetsquery )
		gadgets_output = []
		for gadgetsrow in gadgets:
			up_property = '[[MediaWiki:%s|%s]]' % (gadgetsrow[0], gadgetsrow[0].split('gadget-', 1)[1])
			count = gadgetsrow[1]
			table_row = u'''\
| %s
| %s
|-''' % (up_property, count)
			gadgets_output.append(table_row)
		contents = template % ( self.Wiki.getDataAsOf(), '\n'.join(gender_output), '\n'.join(language_output), '\n'.join(skin_output), '\n'.join(gadgets_output) )
		self.Wiki.outputToWiki( title, contents )

if __name__ == "__main__":
	print "This module should not be called directly! Please use dbr.py to run the database reports."