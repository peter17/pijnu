# -*- coding: utf8 -*-
from __future__ import print_function

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
SEP			: ' '
DOT			: '.'
digit		: [0..9]
integer		: digit+
real		: integer DOT integer?
number		: real / integer
numbers		: number (SEP number)*

"""

from pijnu import *

### title: numbers ###
###   <toolset>
def doAddition(node):
	(n1,n2) = (node[0].value,node[1].value)
	node.value = int(n1) + int(n2)

###   <definition>
PLUS = Char('+')(drop)
digit = Klass(format='[0..9]', charset='0123456789')
integer = Repetition(digit, numMin=1,numMax=False, format='digit+')(join)
addition = Sequence([integer, PLUS, integer])(doAddition)

additionParser = Parser(vars(), 'addition', 'addition', 'None')

s = "22+333"
print(additionParser.match(s))
