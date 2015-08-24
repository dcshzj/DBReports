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

class DBRsimplewiki:
	def __init__( self, db='' ):
		self.dbquery = DBRCore.DBQuery( db )
		self.remotequery = DBRCore.DBQuery( 'simplewiki' )
		self.Wiki = DBRCore.Wiki( db )

	def getPageTitle( self, pageid ):
		query = "SELECT page_namespace, page_title FROM page WHERE page_id='%s';" % ( pageid )
		results = self.remotequery.execute( query )
		for result in results:
			if ( result[0] == 6 or result[0] == 14 ):
				output = ':{{subst:ns:%s}}:%s' % ( result[0], result[1].decode( 'utf8' ) )
			elif ( result[0] == 0 ):
				output = '%s' % ( result[1].decode( 'utf8' ) )
			else:
				output = '{{subst:ns:%s}}:%s' % ( result[0], result[1].decode( 'utf8' ) )
		return output

	def lowerCase( self, text ):
		if not text:
			return 
		else:
			return text[0].lower() + text[1:]

	def execute( self ):
		title = "Interwiki links from Simple English Wikipedia"
		moveherequery = "SELECT cl_from FROM categorylinks WHERE cl_to='Move_to_Wiktionary' ORDER BY cl_from;"
		wiktquery = "SELECT tl_from FROM templatelinks WHERE tl_title='Wiktionary' AND tl_from_namespace='0' ORDER BY tl_from;"
		parquery = "SELECT tl_from FROM templatelinks WHERE tl_title='EnWiktionary' AND tl_from_namespace='0' ORDER BY tl_from;"
		template = '''The list of pages that the [[w:|Simple English Wikipedia]] says we have and may contain blue links. Note that this is ''\'automatically generated''\' and does not recognise proper nouns, instead only getting the first letter to be lower-case, please use this page with care.

Data as of <onlyinclude>%s</onlyinclude>.

== Pages that needs to be moved here ==
:''These pages are in [[w:Category:Move to Wiktionary|Category:Move to Wiktionary]] and should be [[Special:Import|imported here]]''
%s

== Pages that link to Template:Wiktionary ==
:''These pages uses the template [[w:Template:Wiktionary|<nowiki>{{</nowiki>Wiktionary}}]]''
%s

== Pages that link to Template:EnWiktionary ==
:''These pages uses the template [[w:Template:EnWiktionary|<nowiki>{{</nowiki>EnWiktionary}}]]''
%s

[[Category:Wiktionary database reports|{{SUBPAGENAME}}]]
'''
		movehereresults = self.remotequery.execute( moveherequery )
		movehereoutput = []
		for movehereresult in movehereresults:
			pagetitle = self.getPageTitle( movehereresult[0] )
			head, sep, tail = pagetitle.partition( '_(' ) # Removes existence of brackets (disambiguation style)
			movehererow = "[[%s]] - " % ( self.lowerCase( head ) )
			movehereoutput.append( movehererow )

		wiktresults = self.remotequery.execute( wiktquery )
		wiktoutput = []
		for wiktresult in wiktresults:
			pagetitle = self.getPageTitle( wiktresult[0] )
			head, sep, tail = pagetitle.partition( '_(' ) # Removes existence of brackets (disambiguation style)
			wiktrow = "[[%s]] - " % ( self.lowerCase( head ) )
			wiktoutput.append( wiktrow )

		parresults = self.remotequery.execute( parquery )
		paroutput = []
		for parresult in parresults:
			pagetitle = self.getPageTitle( parresult[0] )
			head, sep, tail = pagetitle.partition( '_(' ) # Removes existence of brackets (disambiguation style)
			parrow = "[[%s]] - " % ( self.lowerCase( head ) )
			paroutput.append( parrow )

		contents = template % ( self.Wiki.getDataAsOf(), ''.join( movehereoutput )[:-3], ''.join( wiktoutput )[:-3], ''.join( paroutput )[:-3] )
		self.Wiki.outputToWiki( title, contents )

if __name__ == "__main__":
	print "This module should not be called directly! Please use dbr.py to run the database reports."