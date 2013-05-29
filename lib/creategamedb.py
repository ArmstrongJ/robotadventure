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

from gamedb import *
import sqlite3
import time

class HoldRoom:
    def __init__(self,id):
        self.name = 'empty'
        self.description = 'empty'
        self.away_description = None
        self.id = id
        self.n = None
        self.s = None
        self.e = None
        self.w = None
        self.u = None
        self.d = None
        
    def getTuple(self):
        return (self.id,self.name,self.description,self.away_description,self.n,self.s,self.e,self.w,self.u,self.d)

def conjugate(dir):
    if dir=="north":
        return "south"
    elif dir=="south":
        return "north"
    elif dir=="east":
        return "west"
    elif dir=="west":
        return "east"
    elif dir=="up":
        return "down"
    elif dir=="down":
        return "up"

class CreateDB(GameDB):
    
    def __init__(self):
        GameDB.__init__(self,inplace=True)
        
        self.con.row_factory = sqlite3.Row
        
        cur = self.con.cursor()
        cur.execute('create table if not exists Rooms(id integer unique not null, name text not null, description text not null, away_description text, north integer, south integer, east integer, west integer, up integer, down integer)')
        cur.execute('create table if not exists RoomContents(objectid integer not null, roomid integer not null)')
        cur.execute('create table if not exists Objects(id integer unique not null, name text not null, description text not null, moveable integer, everywhere integer, person integer not null, presence text, explicit integer not null default 1)')
        cur.execute('create table if not exists Combine(id1 integer not null, id2 integer, verb text, result text not null, action text, state integer not null default 0)')
        cur.execute('create table if not exists NPC(id integer unique not null, state integer not null, max integer not null default 1)')
        cur.execute('create table if not exists Talk(id integer not null, verb text, object integer, result text not null)')
        cur.execute('create table if not exists Inventory(id integer unique not null)')
        cur.execute('create table if not exists State(name text unique not null, value text)')
        cur.execute('create table if not exists Block(id integer not null, room1 integer not null, room2 integer not null, description text not null, state integer not null default 1)')
        cur.execute('create table if not exists Synonyms(spoken text not null,name text not null)')
        cur.execute('create table if not exists Verbonyms(spoken text not null,name text not null)')
                
        self.lasttime = 0
        if self.getStart():
            self.getRoom(self.getStart())
        else:
            self.newRoom()

    def getDirectionId(self,dir):
        if dir=="north":
            return self.template.n
        elif dir=="south":
            return self.template.s
        elif dir=="east":
            return self.template.e
        elif dir=="west":
            return self.template.w
        elif dir=="up":
            return self.template.u
        elif dir=="down":
            return self.template.d
        
    def move(self,dir):
        self.saveRoom()
        if self.getDirectionId(dir):
            self.getRoom(self.getDirectionId(dir))
        else:
            originaltemplate = self.template
            self.newRoom()
            self.setId(dir,self.template.id,originaltemplate)
            self.setId(conjugate(dir),originaltemplate.id)
            self.saveRoom(originaltemplate)
            
        self.room = self.template.id
        
        return MOVE_OK
    
    def setId(self,dir,id,template=None):
        if template == None:
            template = self.template
        
        if dir=="north":
            template.n = id
        elif dir=="south":
            template.s = id
        elif dir=="east":
            template.e = id
        elif dir=="west":
            template.w = id
        elif dir=="up":
            template.u = id
        elif dir=="down":
            template.d = id
    
    def getRoomName(self):
        return self.template.name
    
    def getRoomDescription(self):
        return self.template.description
    
    def setRoomName(self,value):
        self.template.name = value
    
    def setRoomDescription(self,value):
        self.template.description = value
        
    def setRoomAwayDescription(self,value):
        if value == 'none':
            self.template.away_description = None
        else:
            self.template.away_description = value
    
    def getNewUID(self):
        uid = int(time.mktime(time.gmtime()))
        if uid == self.lasttime:
            self.lasttime = self.lasttime + 1
        else:
            self.lasttime = uid
            
        return self.lasttime
    
    def newRoom(self):
        self.template = HoldRoom(self.getNewUID())
        
    def saveRoom(self,room=None):
        cur = self.con.cursor()
        if not room:
            room = self.template
        cur.execute("insert or replace into Rooms(id,name,description,away_description,north,south,east,west,up,down) values(?,?,?,?,?,?,?,?,?,?)",
                    room.getTuple())
        self.con.commit()
    
    def getNeighbors(self):
        descriptions = []
        cur = self.con.cursor()
        for id in (self.template.n,self.template.s,self.template.e,self.template.w,self.template.u,self.template.d):
            cur.execute("select name from Rooms where id=?",(id,))
            name = "None"
            for value in cur:
                name = value[0]
                break
            descriptions.append(name)
        
        return descriptions
    
    def object(self,name,desc,presence,glob=False):
        everywhere = False
        if glob:
            everywhere=True
        id = self.getNewUID()
        cur = self.con.cursor()
        cur.execute("insert into Objects(id,name,description,presence,moveable,person,everywhere) values(?,?,?,?,?,?,?)",
                    (id,name,desc,presence,1,0,everywhere))
        cur.execute("insert into RoomContents(objectid,roomid) values(?,?)",(id,self.template.id))
    
    def person(self,name,desc,presence):
        id = self.getNewUID()
        cur = self.con.cursor()
        cur.execute("insert into Objects(id,name,description,presence,moveable,person,everywhere) values(?,?,?,?,?,?,?)",(id,name,desc,presence,0,1,0))
        cur.execute("insert into NPC(id,state,max) values(?,?,?)",(id,0,0))
        cur.execute("insert into RoomContents(objectid,roomid) values(?,?)",(id,self.template.id))
    
    def action(self,name,verb,result,action,state=0):
        objid = self.getObjId(name,False)
        if not objid:
            print "Object not found..."
            return
        cur = self.con.cursor()
        cur.execute("insert into Combine(id1,verb,result,action,state) values(?,?,?,?,?)",
                    (objid,verb,result,action,state))
    
    def synonym(self,name,synonym):
        cur = self.con.cursor()
        cur.execute("insert into Synonyms(spoken,name) values(?,?)",(synonym,name))
    
    def verbonym(self,name,synonym):
        cur = self.con.cursor()
        cur.execute("insert into Verbonyms(spoken,name) values(?,?)",(synonym,name))
    
    def actionCombine(self,name1,name2,verb,result,action,state=0):
        id1 = self.getObjId(name1)
        id2 = self.getObjId(name2)
        if not id1:
            print "Object not found: "+name1
            return
        if not id2:
            print "Object not found: "+name2
            return
        
        cur = self.con.cursor()
        cur.execute("insert into Combine(id1,id2,verb,result,action,state) values(?,?,?,?,?,?)",
                    (id1,id2,verb,result,action,state))
            
    
    def setBlock(self,dir,desc):
        id2 = None
        if dir=="n":
            id2 = self.template.n
        elif dir=="s":
            id2 = self.template.s
        elif dir=="e":
            id2 = self.template.e
        elif dir=="w":
            id2 = self.template.w
        elif dir=="u":
            id2 = self.template.u
        elif dir=="d":
            id2 = self.template.d
        if not id2:
            return
        
        cur = self.con.cursor()
        cur.execute("insert into Block(id,room1,room2,description) values(?,?,?,?)",(self.getNewUID(),self.template.id,id2,desc))
    
    def getRoom(self,id):
        cur = self.con.cursor()
        cur.execute("select * from Rooms where id=?",(id,))
        self.template = None
        for room in cur:
            self.template = HoldRoom(id)
            self.template.name = room["name"]
            self.template.description = room["description"]
            self.template.away_description = room["away_description"]
            self.template.n = room["north"]
            self.template.s = room["south"]
            self.template.e = room["east"]
            self.template.w = room["west"]
            self.template.u = room["up"]
            self.template.d = room["down"]
    
    def setStart(self):
        cur = self.con.cursor()
        cur.execute("insert or replace into State(name, value) values('Start',?)",(str(self.template.id),))
    
    def end(self):
        self.saveRoom()
        self.con.commit()
        self.con.close()
        
    
