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

import sqlite3
import tempfile
import shutil
import os
from data import *

MOVE_OK = 'Ok'
MOVE_FAILED = 'Failed'

DEFAULTFILE = 'game.db'

CONTENTS_PREFIX = 'There is a '
CONTENTS_SUFFIX = ' here.'

def getSafeDirection(string):
    if string=='n':
        return 'north'
    elif string=='s':
        return 'south'
    elif string=='e':
        return 'east'
    elif string=='w':
        return 'west'
    elif string=='u':
        return 'up'
    elif string=='d':
        return 'down'
    

class GameDB:
    def __init__(self,filename=None,inplace=False):
        
        if not filename:
            filename = filepath(DEFAULTFILE)
        
        self.con = None
        if not inplace:
            self.tempname = tempfile.mktemp()
        
            shutil.copyfile(filename, self.tempname)
        
            self.con = sqlite3.connect(self.tempname)
        else:
            self.con = sqlite3.connect(filename)
            
        self.con.isolation_level = None
        
        self.room = self.getStart()
    
    def getRoomName(self):
        cur = self.con.cursor()
        cur.execute("select name from Rooms where id=?",(self.room,))
        for row in cur:
            return row[0]
        
    def getRoomDescription(self):
        cur = self.con.cursor()
        cur.execute("select description from Rooms where id=?",(self.room,))
        for row in cur:
            return row[0] 
        
    def getNorthDescription(self):
        return self.getDirection("north")
    
    def getSouthDescription(self):
        return self.getDirection("south")
    
    def getEastDescription(self):
        return self.getDirection("east")
    
    def getWestDescription(self):
        return self.getDirection("west")
    
    def getUpDescription(self):
        return self.getDirection("up")

    def getDownDescription(self):
        return self.getDirection("down")
    
    def moveNorth(self):
        return self.move("north")
    
    def moveSouth(self):
        return self.move("south")
    
    def moveEast(self):
        return self.move("east")
    
    def moveWest(self):
        return self.move("west")
    
    def moveUp(self):
        return self.move("up")
    
    def moveDown(self):
        return self.move("down")
    
    def move(self,dir):
        cur = self.con.cursor()
        id = self.getDirectionId(dir)
        if id:
            
            if self.getBlock(id):
                return self.getBlock(id)
            
            self.room = id
            return MOVE_OK
        return MOVE_FAILED
    
    def clearSynonyms(self,string):
        cur = self.con.cursor()
        cur.execute('select name from Objects inner join RoomContents on id=objectid where roomid=?',(self.room,))
        for object in cur:
            oc = self.con.cursor()
            oc.execute('select spoken,length(spoken) from Synonyms where name=? order by length(spoken) desc',(object[0],))
            for item in oc:
                #print item[0]+':'+object[0]
                if string.find(' '+item[0]) >= 0:
                    string = string.replace(' '+item[0],' '+object[0])
                    break
                
        cur.execute('select name from Objects inner join Inventory on Objects.id=Inventory.id')
        for object in cur:
            oc = self.con.cursor()
            oc.execute('select spoken,length(spoken) from Synonyms where name=? order by length(spoken) desc',(object[0],))
            for item in oc:
                #print item[0]+':'+object[0]
                if string.find(' '+item[0]) >= 0:
                    string = string.replace(' '+item[0],' '+object[0])
                    break
                
        return string
        
    def getDirectionId(self,dir):
        cur = self.con.cursor()
        cur.execute("select %s from Rooms where id=?" % dir,(self.room,))
        for row in cur:
            return row[0]
        return None
        
    def getDirection(self, dir):
        id = self.getDirectionId(dir)
        cur = self.con.cursor()
        if id:        
            cur.execute("select away_description from Rooms where id=?",(id,))
            for row in cur:
                return row[0]
            
        return None
        
    def getRoomContents(self):
        rooms = []
        cur = self.con.cursor()
        cur.execute("select objectid from RoomContents where roomid=?",(self.room,))
        for row in cur:
            oc = self.con.cursor()
            oc.execute("select name,presence,explicit from Objects where id=?",(row[0],))
            for row in oc:
                if row[2]==0:
                    continue
                if row[1]:
                    rooms.append(row[1])
                else:
                    rooms.append(CONTENTS_PREFIX+row[0]+CONTENTS_SUFFIX)
                break
        return rooms
    
    def getInventory(self):
        inv = []
        cur = self.con.cursor()
        cur.execute("select name from Objects outer join Inventory on Objects.id=Inventory.id")
        for row in cur:
            inv.append(row[0])
        return inv
    
    def lookAt(self,obj):
        cur = self.con.cursor()
        cur.execute("select name,description from RoomContents inner join Objects on Objects.id=RoomContents.objectid where roomid=? and name=?",(self.room,obj))
        for row in cur:
            return row[1]
        return None
    
    def pickUp(self,name):
        cur = self.con.cursor()
        cur.execute("select id,moveable,person from Objects outer join RoomContents on Objects.id = RoomContents.objectid where name=? and roomid=?",(name,self.room))
        id = None
        for obj in cur:
            id = obj[0]
            if obj[2] == 1:
                return "I don't think %s would appreciate that." % name
            if obj[1] == 0:
                return "%s can't be moved." % name.title()
            break
        
        if id == None:
            return None
        
        cur.execute("delete from RoomContents where objectid=?",(id,))
        cur.execute("insert into Inventory(id) values(?)",(id,))
        return True
    
    def drop(self,name):
        id = None
        cur = self.con.cursor()
        cur.execute("select Objects.id from Objects outer join Inventory on Objects.id = Inventory.id where name=?",(name,))
        for obj in cur:
            id = obj[0]
            
        if id == None:
            return False
        
        cur.execute("delete from Inventory where id=?",(id,))
        cur.execute("insert into RoomContents(objectid,roomid) values(?,?)",(id,self.room))
        return True
    
    def getObjId(self,name,hereonly=False):
        cur = self.con.cursor()
        cur.execute("select Objects.id from Objects outer join Inventory on Objects.id = Inventory.id where name=?",(name,))
        for obj in cur:
            return obj[0]
        cur.execute("select id from Objects outer join RoomContents on Objects.id = RoomContents.objectid where name=? and roomid=?",(name,self.room))
        for obj in cur:
            return obj[0]
        
        cur.execute("select id from Objects where name=? and everywhere=1",(name,))
        for obj in cur:
            return obj[0]
           
        if hereonly:
            return None
            
        cur.execute("select id from Objects where name=?",(name,))
        for obj in cur:
            return obj[0]
        
        return None

    def getBlock(self,id2):
        cur = self.con.cursor()
        cur.execute('select state, description from Block where (room1=? and room2=?) or (room1=? and room2=?)',(self.room,id2,id2,self.room))
        for row in cur:
            if row[0] == 1:
                return row[1]
            else:
                return None
        return None
    
    def unblock(self,blockid):
        cur = self.con.cursor()
        cur.execute('update Block set state=0 where id=?',(blockid,))
    
    def getResult(self,obj1,obj2=None,verb=None):
        id1 = self.getObjId(obj1,True)
        id2 = None
        if obj2:
            id2 = self.getObjId(obj2,True)
            #print obj2,id2
        
        return self.fromCombine(id1,id2,verb,'result')

    def increment(self,incid):
        cur = self.con.cursor()
        
        state = 0
        max = 1
        
        try:
            incid=int(incid)
        except ValueError:
            incid = self.getObjId(incid,False)
        
        cur.execute('select state,max from NPC where id=?',(incid,))
        for row in cur:
            state = row[0]
            max = row[1]
        
        state = state + 1
        if state <= max:
            try:
                cur.execute('update NPC set state=? where id=?',(state,incid))
            except:
                pass
    
    def remove(self,incid):
        try:
            incid=int(incid)
        except ValueError:
            incid = self.getObjId(incid,False)
            
        cur = self.con.cursor()
        cur.execute('delete from Inventory where id=?',(incid,))
        
    def to_inv(self,incid):
        try:
            incid=int(incid)
        except ValueError:
            incid = self.getObjId(incid,False)
            
        cur = self.con.cursor()
        cur.execute('insert into Inventory values(?)',(incid,))
        
    def setState(self,incid,state):
        maxstate = 1
        try:
            incid=int(incid)
        except ValueError:
            incid = self.getObjId(incid,False)
        
        cur = self.con.cursor()  
        cur.execute('select state,max from NPC where id=?',(incid,))
        for row in cur:
            state = max(row[0],state)
            maxstate = row[1]
        
        if state <= maxstate:
            try:
                cur.execute('update NPC set state=? where id=?',(state,incid))
            except:
                pass

    def getEnding(self):
        cur = self.con.cursor()  
        cur.execute("select value from State where name='Ending'")
        for row in cur:
            return row[0]
        return 'End Game'
        
    def isEnd(self):
        cur = self.con.cursor()  
        cur.execute("select value from State where name='End'")
        for row in cur:
            try:
                id = int(row[0])
                if self.room == id:
                    return True
            except ValueError:
                return False    
        return False

    def getIntro(self):
        cur = self.con.cursor()
        cur.execute('select value from State where name=?',('Intro',))
        for row in cur:
            return row[0]
        return ' '

    def getTitle(self):
        cur = self.con.cursor()
        cur.execute('select value from State where name=?',('Title',))
        for row in cur:
            return row[0]
        return ' '

    def getAction(self,obj1,obj2=None,verb=None):
        id1 = self.getObjId(obj1,True)
        id2 = None
        if obj2:
            id2 = self.getObjId(obj2,True)
        
        return self.fromCombine(id1,id2,verb,'action')

    def getState(self,obj):
        cur = self.con.cursor()
        cur.execute('select state from NPC where id=?',(obj,))
        for row in cur:
            return row[0]
        return 0;

    def fromCombine(self,obj1,obj2,verb,column):
        cur = self.con.cursor()
        
        state1 = self.getState(obj1)
        state2 = self.getState(obj2)
        state = max(state1,state2)
        
        if obj1 and obj2 and verb:
            cur.execute("select %s from Combine where ((id1=? and id2=?) or (id1=? and id2=?)) and verb=? and state<=? order by state desc" % column,(obj1,obj2,obj2,obj1,verb,state))

        elif obj1 and obj2:
            cur.execute("select %s from Combine where (id1=? and id2=?) or (id1=? and id2=?) and state<=? order by state desc" % column,(obj1,obj2,obj2,obj1,state))

        elif obj1 and verb:
            cur.execute("select %s from Combine where id1=? and verb=? and state<=? order by state desc " % column,(obj1,verb,state))

        for row in cur:
            return row[0]
        return None

    def checkVerb(self,spoken):
        if not spoken:
            return None
        
        cur = self.con.cursor()
        cur.execute("select name from Verbonyms where spoken=?",(spoken,))
        for row in cur:
            return row[0]
        return spoken
    
    def use(self,obj1,obj2):
        id2 = getObjId(obj2,True)
        if not id1 or not id2:
            return None     
        return None
    
    def getStart(self):
        cur = self.con.cursor()
        cur.execute("select value from State where name='Start'")
        for row in cur:
            try:
                return int(row[0])
            except ValueError:
                pass
            
        return None
    
    def setStart(self):
        cur = self.con.cursor()
        cur.execute("update State set value=? where name='Start'",(self.room,))
        
    
    def save(self,filename):
        self.setStart()
        self.con.commit()
        try:
            shutil.copyfile(self.tempname, filename)
        except:
            print "WARN: an error may have occured saving to "+filename
            return False
        return True
        
    def end(self):
        self.con.close()
        
        try:
            os.delete(self.tempname)
        except:
            pass
        
