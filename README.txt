Murder in the Park - A Robotic Mystery
======================================

Entry in PyWeek #6  <http://www.pyweek.org/6/>
Team: PrintStar Zero
Members: PrintStar


DEPENDENCIES:

You might need to install some of these before running the game:

  Python 2.5:     http://www.python.org/
  
Note that this game makes heavy use of the sqlite3 module, which is
part of the Python 2.5 standard library.  If you receive an error
complaining about the module "_sqlite3", it has not been compiled 
into the runtime library.  


RUNNING THE GAME:

Open a terminal / console and "cd" to the game directory and run:

  python run_game.py
  
Double-clicking on run_game.py should work fine in Windows.  This game 
is a text adventure and will attempt to use curses on platforms where
available. 

To force the game to start without curses (for example if your terminal 
is not supported, use the following command:

  python run_game.py --nocurses
  
Windows users have the option of downloading and running the py2exe 
version.  Simply click on run_game.exe to start the game.

HOW TO PLAY THE GAME:

The game operates similar to other text adventures or interactive 
fiction games.  There is a command prompt and some common commands that 
you can type.  The intrepretter understands _very_ simplistic english 
commands:

    n,s,e,w         Move north, south, east, or west
    
    u,d             Move up or down
    
    look            Looks around you
    
    look <n,s,e,w>  Look in a given direction
    
    get <?>         Picks up an item
    
    look at <?>     Looks at whatever you want
    
    ask <?>         Ask a character about something
      about <?>
      
    talk to <?>     Talk to a character
    
    give <?>        Give an item to a character
      to <?>
      
    inv             Show your current inventory
    
    save            Saves your game
    
    load            Loads a saved game
    
    quit            Exits the game

Some other verbs and actions may also work.  The list above is just the 
most common.  The best thing you can do is try.  The game is not 
exhaustive or comprehensive, so there might be some misunderstanding by 
the interpretter.

LICENSE:

This game and all its content (including the game database) is:

Copyright 2008 Jeffrey Armstrong (a.k.a. PrintStar)
Licensed under the GNU General Public License Version 3

And the formal text:

Murder in the Park - A Robotic Mystery
Copyright (C) 2008 Jeffrey Armstrong (a.k.a. PrintStar)
http://jeff.rainbow-100.com/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

A full version of the license terms is available in LICENSE.

