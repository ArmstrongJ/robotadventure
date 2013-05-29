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

import sys
import textwrap
from gamecmd import *

TERMWIDTH=80

class FakeStdIO(object):
    def __init__(self):
        self.stdin = sys.stdin
        self.stdout = sys.stdout

    def write(self, str):
        if len(str) >= TERMWIDTH:
            for line in textwrap.wrap(str,TERMWIDTH-2):
                self.stdout.write(line)
                self.stdout.write("\n")
        else:
            self.stdout.write(str)
        
    def readline(self):
        return self.stdin.readline()
    
def launch(cmdparser):
    io = FakeStdIO()
    sys.stdin = io
    sys.stdout = io
    cmdparser.stdout = io
    cmdparser.cmdloop()