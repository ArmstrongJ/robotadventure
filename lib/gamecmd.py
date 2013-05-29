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

import cmd
from gamedb import *
from prep import *
from unsure import *
from custom import *

PROMPT = '>> '

class GameCmd(cmd.Cmd):
    def __init__(self,db=None):
        cmd.Cmd.__init__(self)
        
        if db:
            self.db = db
        else:
            try:
                self.db = GameDB()
            except IOError:
                print 'Error loading default game file...'
    
        self.prompt = PROMPT
    
    def do_n(self,args):
        """Moves north..."""
        success = self.db.moveNorth()
        self.ackMove(success)
        
    def do_s(self,args):
        """Moves south..."""
        success = self.db.moveSouth()
        self.ackMove(success)
    
    def do_e(self,args):
        """Moves east..."""
        success = self.db.moveEast()
        self.ackMove(success)
    
    def do_w(self,args):
        """Moves west..."""
        success = self.db.moveWest()
        self.ackMove(success)
        
    def do_u(self,args):
        """Moves up..."""
        success = self.db.moveUp()
        self.ackMove(success)
    
    def do_d(self,args):
        """Moves down..."""
        success = self.db.moveDown()
        self.ackMove(success)
    
    def do_north(self,args):
        """Moves north..."""
        success = self.db.moveNorth()
        self.ackMove(success)
        
    def do_south(self,args):
        """Moves south..."""
        success = self.db.moveSouth()
        self.ackMove(success)
    
    def do_east(self,args):
        """Moves east..."""
        success = self.db.moveEast()
        self.ackMove(success)
    
    def do_west(self,args):
        """Moves west..."""
        success = self.db.moveWest()
        self.ackMove(success)
        
    def do_up(self,args):
        """Moves up..."""
        success = self.db.moveUp()
        self.ackMove(success)
    
    def do_down(self,args):
        """Moves down..."""
        success = self.db.moveDown()
        self.ackMove(success)
    
    def do_look(self,args):
        """Looks at an object or just around in general"""
        if len(args.strip()) == 0:
            self.outputRoom()
            return
        
        cleaner = removePrep(args)
        
        if isDirection(cleaner.strip()):
            self.outputLook(cleaner.strip())
        else:
            #print cleaner.strip()
            self.outputLookAt(self.db.lookAt(cleaner.strip()))
    
    def do_examine(self,args):
        if len(args.strip())==0:
            print "Examine what?"
        
        self.do_look('at '+args.strip())
    
    def do_i(self,args):
        """List inventory..."""
        inv = self.db.getInventory()
        if len(inv) == 0:
            'You currently have no items in your inventory'
            return
        print 'Current Inventory:'
        for x in inv:
            print '  '+x
        
    def do_inv(self,args):
        """List inventory..."""
        self.do_i(args)
        
    def do_inventory(self,args):
        """List inventory..."""
        self.do_i(args)
        
    def do_get(self,args):
        """Picks up an item in the room..."""
        success = self.db.pickUp(args)
        if not success:
            print "I don't see any %s to pick up" % args
        elif success == True:
            print 'Picked up %s' % args
        else:
            print success
            
    def do_drop(self,args):
        """Drops an inventory item"""
        success = self.db.drop(args)
        if not success:
            print "You're not carrying %s" % args
        elif success == True:
            print "Dropped %s" % args
    
    def do_exit(self,args):
        """Quits the game..."""
        return self.do_quit(args)
        
    def do_quit(self,args):
        """Quits the game..."""
        self.db.end()
        return -1
    
    def do_save(self,args):
        """Saves the game to a specified file"""
        if len(args.strip()) == 0:
            print "Please include a filename - save <filename>"
        else:
            success = self.db.save(args.strip())
            if success:
                print "Game saved successfully"
            else:
                print "Unknown error while saving..."
    
    def do_load(self,args):
        """Loads the game from a specified file"""
        if len(args.strip()) == 0:
            print "Please include a filename - load <filename>"
        else:
            backupdb = self.db
            try:
                self.db = GameDB(args.strip())
                print "Loading successful!"
                print
                self.ackMove(MOVE_OK)
                backupdb.end()
            except:
                self.db = backupdb
                print "Loading failed for unknown reasons..."
                
    def do_xyzzy(self,args):
        """..."""
        print "The air shimmers with magic..."
        print "Something big is about to happen..."
        print "..."
        print "You hear a distant sigh of disgust, but nothing else happens."
    
    def default(self,args):
        """For unrecognized commands"""
        
        ret = False
        
        if len(args.strip()) > 0:
            (verb,obj1,obj2) = parseSentence(args)
            #print verb,obj1,obj2
            ret = handle(self.db,verb,obj1,obj2)            
        
        if not ret:
            print getUnkownCmd()
        else:
            print ret
    
    def outputRoom(self):
        print '* '+self.db.getRoomName()+' *'
        print self.db.getRoomDescription()
        
        for item in self.db.getRoomContents():
            print item
        #print
    
    def outputLook(self,dir):
        desc = self.db.getDirection(getSafeDirection(dir))
        if desc:
            print desc
        else:
            print "It's a little foggy..."
                
    def outputLookAt(self,text):
        if text:
            print text
        else:
            print "Excuse me?"            
    
    def precmd(self,line):
        return self.db.clearSynonyms(line)
    
    def postcmd(self,stop,line):
        if stop:
            return stop
        
        if self.db.isEnd():
            for line in self.db.getEnding().splitlines():
                print line
                print "Press ENTER to continue..."
                self.stdin.readline()
            self.db.end()
            return True
        return False
    
    def preloop(self):
        for line in self.db.getIntro().splitlines():
            print line
            print "Press ENTER to continue..."
            self.stdin.readline()
        
        print
        
        for line in self.db.getTitle().splitlines():
            print line
            
        print
        
        self.outputRoom()
        
    def ackMove(self,success=MOVE_OK):
        if success==MOVE_OK:
            self.outputRoom()
        elif success==MOVE_FAILED:
            print 'That way is blocked...'
        else:
            print success
    
