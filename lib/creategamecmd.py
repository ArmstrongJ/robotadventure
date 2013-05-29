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


from creategamedb import *
from gamecmd import *

class CreateCmd(GameCmd):
    def __init__(self):
        GameCmd.__init__(self,CreateDB())
    
    def do_where(self,args):
        names = self.db.getNeighbors()
        print 'n: '+names[0]
        print 's: '+names[1]
        print 'e: '+names[2]
        print 'w: '+names[3]
        print 'u: '+names[4]
        print 'd: '+names[5]
        
    def do_quit(self,args):
        self.db.end()
        return -1
    
    def do_name(self,args):
        self.db.setRoomName(args)
    
    def do_desc(self,args):
        self.db.setRoomDescription(args)
    
    def do_awaydesc(self,args):
        self.db.setRoomAwayDescription(args)
        
    def do_start(self,args):
        self.db.setStart()
        
    def do_block(self,args):
        args = args.strip()
        dir = args[0]
        desc = args[2:].strip()
        self.db.setBlock(dir,desc)
    
    def do_synonym(self,args):
        elements = args.strip().split(' ',1)
        self.db.synonym(elements[0],elements[1])
    
    def do_verbonym(self,args):
        elements = args.strip().split(' ',1)
        self.db.verbonym(elements[0],elements[1])    
    
    def do_person(self,args):
        """person name,desc,presence"""
        elements = args.strip().split(',')
        try:
            self.db.person(elements[0],elements[1],elements[2])
        except IndexError:
            print "Missing argument..."
    
    def do_object(self,args):
        """object name,desc,presence,[0 or 1 for global]"""
        elements = args.strip().split(',')
        if len(elements)==3:
            self.db.object(elements[0],elements[1],elements[2])
        elif len(elements)==4:
            self.db.object(elements[0],elements[1],elements[2],int(elements[3]))
        else:
            print "Argument error..."
            
    def do_action(self,args):
        """action name,verb,result,action,[state (0 is default)]"""
        elements = args.strip().split(',')
        if len(elements)==4:
            self.db.action(elements[0],elements[1],elements[2],elements[3])
        elif len(elements) == 5:
            self.db.action(elements[0],elements[1],elements[2],elements[3],int(elements[4]))
        else:
            print "Argument error..."
            
    def do_combine(self,args):
        """combine name1,name2,verb,result,action,[state (0 is default)]"""
        elements = args.strip().split(',')
        if len(elements)==5:
            self.db.actionCombine(elements[0],elements[1],elements[2],elements[3],elements[4])
        elif len(elements)==6:
            self.db.actionCombine(elements[0],elements[1],elements[2],elements[3],elements[4],int(elements[5]))
        else:
            print "Argument error..."
        