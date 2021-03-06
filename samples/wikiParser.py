# -*- coding: utf8 -*-

'''
Copyright 2009 Denis Derman <denis.spir@gmail.com> (former developer)
Copyright 2011-2012 Peter Potrowl <peter017@gmail.com> (current developer)

This file is part of Pijnu.

Pijnu is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pijnu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with Pijnu.  If not, see <http://www.gnu.org/licenses/>.
'''

"""
<definition>
# codes
	DISTINCT		: "//"								: drop
	IMPORTANT		: "!!"								: drop
	WARNING			: "**"								: drop
	ESCAPE			: '~'
# character expression
	escChar			: ESCAPE ('*' / '!' / '/')
	rawChar			: [\x20..\xff  !!/!*]
	lineChar		: [\x20..\xff]
	rawText			: rawChar+							: join
# text
	distinctText	: DISTINCT inline DISTINCT			: liftValue
	importantText	: IMPORTANT inline IMPORTANT		: liftValue
	warningText	: WARNING inline WARNING		: liftValue
	styledText		: distinctText / importantText / warningText
	text			: styledText / rawText
	inline			: text+								: @
# line types
	LF				: '
'
	CR				: ''
	EOL				: (LF/CR)+								: drop
	BULLETLIST		: "*"									: drop
	NUMBERLIST		: "#"									: drop
	TITLE			: "="									: drop
	paragraf		: !(BULLETLIST/NUMBERLIST) inline EOL	: liftValue
	paragrafs		: paragraf+
	bulletListItem	: BULLETLIST inline EOL					: liftValue
	bulletList		: bulletListItem+
	numberListItem	: NUMBERLIST inline EOL					: liftValue
	numberList		: numberListItem+
	blankLine		: EOL
	body			: (bulletList / numberList / paragrafs / blankLine)+
	#body			: (bulletListItem / numberListItem / paragraf / blankLine)+
	title			: TITLE inline EOL 					: liftValue
	text			: blankLine* title? body

"""



from pijnu.library import *

wikiParser = Parser()
state = wikiParser.state

### title: wiki ###
###   <definition>
# recursive pattern(s)
inline = Recursive()
# codes
DISTINCT = Word('//', format='"//"')(drop)
IMPORTANT = Word('!!', format='"!!"')(drop)
WARNING = Word('**', format='"**"')(drop)
ESCAPE = Char('~', format="'~'")
# character expression
escChar = Sequence([ESCAPE, Choice([Char('*', format="'*'"), Char('!', format="'!'"), Char('/', format="'/'")], format="'*' / '!' / '/'")], format="ESCAPE ('*' / '!' / '/')")
rawChar = Klass(format='[\\x20..\\xff  !!/!*]', charset=' "#$%&\'()+,-.0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff')
lineChar = Klass(format='[\\x20..\\xff]', charset=' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff')
rawText = Repetition(rawChar, numMin=1,numMax=False, format='rawChar+')(join)
# text
distinctText = Sequence([DISTINCT, inline, DISTINCT], format='DISTINCT inline DISTINCT')(liftValue)
importantText = Sequence([IMPORTANT, inline, IMPORTANT], format='IMPORTANT inline IMPORTANT')(liftValue)
warningText = Sequence([WARNING, inline, WARNING], format='WARNING inline WARNING')(liftValue)
styledText = Choice([distinctText, importantText, warningText], format='distinctText / importantText / warningText')
text = Choice([styledText, rawText], format='styledText / rawText')
inline **= Repetition(text, numMin=1,numMax=False, format='text+')
# line types
LF = Char('\n', format="'\n'")
CR = Char('\r', format="'\r'")
EOL = Repetition(Choice([LF, CR], format='LF/CR'), numMin=1,numMax=False, format='(LF/CR)+')(drop)
BULLETLIST = Word('*', format='"*"')(drop)
NUMBERLIST = Word('#', format='"#"')(drop)
TITLE = Word('=', format='"="')(drop)
paragraf = Sequence([NextNot(Choice([BULLETLIST, NUMBERLIST], format='BULLETLIST/NUMBERLIST'), format='!(BULLETLIST/NUMBERLIST)'), inline, EOL], format='!(BULLETLIST/NUMBERLIST) inline EOL')(liftValue)
paragrafs = Repetition(paragraf, numMin=1,numMax=False, format='paragraf+')
bulletListItem = Sequence([BULLETLIST, inline, EOL], format='BULLETLIST inline EOL')(liftValue)
bulletList = Repetition(bulletListItem, numMin=1,numMax=False, format='bulletListItem+')
numberListItem = Sequence([NUMBERLIST, inline, EOL], format='NUMBERLIST inline EOL')(liftValue)
numberList = Repetition(numberListItem, numMin=1,numMax=False, format='numberListItem+')
blankLine = copy(EOL)
body = Repetition(Choice([bulletList, numberList, paragrafs, blankLine], format='bulletList / numberList / paragrafs / blankLine'), numMin=1,numMax=False, format='(bulletList / numberList / paragrafs / blankLine)+')
	#body			: (bulletListItem / numberListItem / paragraf / blankLine)+
title = Sequence([TITLE, inline, EOL], format='TITLE inline EOL')(liftValue)
text = Sequence([Repetition(blankLine, numMin=False,numMax=False, format='blankLine*'), Option(title, format='title?'), body], format='blankLine* title? body')


wikiParser._recordPatterns(vars())
wikiParser._setTopPattern("text")
wikiParser.grammarTitle = "wiki"
wikiParser.fileName = "wikiParser.py"
