# Murder in the Park - A Robotic Mystery
# Copyright (C) 2008 Jeffrey Armstrong (a.k.a. PrintStar)
# http://jeff.rainbow-100.com/
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# A full version of the license terms is available in LICENSE.

PREPOSITIONS = ['at',
'with',
'in',
'to',
'on',
'inside',
'into',
'onto',
'about',
'the',
'a',
'an',
'out']

def removePrep(args):
    words = args.split()
    astr = ''
    for word in words:
        try:
            PREPOSITIONS.index(word)
        except ValueError:
            astr = astr + word + ' '
            
    return astr.strip()

def parseSentence(sentence):
    """Parses the sentence and returns a verb and the two objects (if applicable)"""
    elements = sentence.split()
    verb = elements[0]
    obj1 = None
    obj2 = None
    elements = elements[1:]

    for value in elements:
        try:
            ind = PREPOSITIONS.index(value)
            elements.remove(value)
        except ValueError:
            continue
            
    if len(elements) >= 1:
        obj1 = elements[0]
        
    if len(elements) >= 2:
        obj2 = elements[1]
        
    return (verb,obj1,obj2)
