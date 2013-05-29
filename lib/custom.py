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

import gamedb

NPC_VERBS = ['ask',
'question',
'talk',
'tell',
'say',
'speak',
'show',
'hand',
'give']

DIRECTIONS = ['north','n',
              'west','w',
              'south','s',
              'east','e']

def isDirection(word):
    try:
        DIRECTIONS.index(word)
        return True
    except ValueError:
        return False

def handleVerbOnly(db,verb):
    return None

def parseAction(db,action):
    if not action:
        return
    actions = action.split(';')
    for each in actions:
        each = each.strip()
        components = each.split()
        
        if each.startswith('unblock'):
            db.unblock(components[1])
            
        elif each.startswith('increment'):
            db.increment(components[1])
        
        elif each.startswith('remove'):
            db.remove(components[1])
            
        elif each.startswith('create'):
            db.to_inv(components[1])
            
        elif each.startswith('state'):
            try:
                db.setState(components[1],int(components[2]))
            except ValueError:
                continue


def handle(db,verb,obj1=None,obj2=None):

    verb = db.checkVerb(verb)

    if not obj1 and not obj2:
        return handleVerbOnly(db,verb)
    
    result = db.getResult(obj1,obj2,verb)
    action = db.getAction(obj1,obj2,verb)
    parseAction(db,action)
    return result

