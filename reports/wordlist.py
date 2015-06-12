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

class DBRwordlist:
	def __init__( self, db='' ):
		self.dbquery = DBRCore.DBQuery( db )
		self.Wiki = DBRCore.Wiki( db )
		self.wordlists = [
			'Academic word list',
			'American Heritage most frequent wordlist',
			'Basic English compound wordlist',
			'Basic English international wordlist',
			'Extended Basic English alphabetical wordlist',
			'Basic English alphabetical wordlist',
			'Basic English ordered wordlist',
			'Basic English picture wordlist',
			'BE850 BNC1000HW list',
			'BNC spoken freq 01',
			'BNC spoken freq 01a',
			'BNC spoken freq 01a HW',
			'BNC spoken freq 01f',
			'BNC spoken freq 01f HW',
			'BNC spoken freq 01HW',
			'BNC spoken freq 01HWC',
			'BNC spoken freq 01n',
			'BNC spoken freq 01n HW',
			'BNC spoken freq 01s',
			'BNC spoken freq 01s HW',
			'BNC spoken freq 02',
			'BNC spoken freq 02a',
			'BNC spoken freq 02a HW',
			'BNC spoken freq 02f',
			'BNC spoken freq 02f HW',
			'BNC spoken freq 02HW',
			'BNC spoken freq 02HWC',
			'BNC spoken freq 02n',
			'BNC spoken freq 02n HW',
			'BNC spoken freq 02s',
			'BNC spoken freq 02s HW',
			'BNC spoken freq 03',
			'BNC spoken freq 03a',
			'BNC spoken freq 03a HW',
			'BNC spoken freq 03f',
			'BNC spoken freq 03f HW',
			'BNC spoken freq 03HW',
			'BNC spoken freq 03HWC',
			'BNC spoken freq 03n',
			'BNC spoken freq 03n HW',
			'BNC spoken freq 03s',
			'BNC spoken freq 03s HW',
			'BNC spoken freq 04',
			'BNC spoken freq 04a',
			'BNC spoken freq 04a HW',
			'BNC spoken freq 04f',
			'BNC spoken freq 04f HW',
			'BNC spoken freq 04HW',
			'BNC spoken freq 04HWC',
			'BNC spoken freq 04n',
			'BNC spoken freq 04n HW',
			'BNC spoken freq 04s',
			'BNC spoken freq 04s HW',
			'General Service List',
			'Irregular Verb List',
			'Most frequent 1000 words in English',
			'Simple English word list'
		]

	def execute( self ):
		title = "Word lists completion status"
		template = '''The completion status of [[{{subst:SITENAME}}:Word lists|word lists]]; data as of <onlyinclude>%s</onlyinclude>.

{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! No.
! Word list
! Blue links
! Total links
! Completion percent
|-
%s
|}

[[Category:{{subst:SITENAME}} database reports|{{SUBPAGENAME}}]]
'''
		getpagelist = "SELECT page_title FROM page WHERE page_namespace='0';"
		pagelist = self.dbquery.execute( getpagelist )
		listofpages = []
		for page in pagelist:
			listofpages.append( page[0] )
		output = []
		i = 1
		for wordlist in self.wordlists:
			wordlist = wordlist.replace( " ", "_" );
			getpageid = "SELECT page_id FROM page WHERE page_namespace='4' AND page_title='%s' LIMIT 1;" % ( wordlist )
			pageid = self.dbquery.execute( getpageid )
			for page in pageid:
				getlinks = "SELECT pl_title FROM pagelinks WHERE pl_namespace='0' AND pl_from='%s';" % ( page[0] )
			links = self.dbquery.execute( getlinks )
			e = 0
			t = 0
			for link in links:
				t += 1
				link = link[0]
				if ( link in listofpages ):
					e += 1
				else:
					continue
			percent = 100 * float(e)/float(t)
			tablerow = "| %d\n| [[{{subst:SITENAME}}:%s]]\n| %d\n| %d\n| %d%%\n|-" % ( i, wordlist, e, t, percent )
			output.append( tablerow )
			i += 1
		contents = template % ( self.Wiki.getDataAsOf(), '\n'.join( output ) )
		self.Wiki.outputToWiki( title, contents )

if __name__ == "__main__":
	print "This module should not be called directly! Please use dbr.py to run the database reports."