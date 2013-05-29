#! /usr/bin/env python
'''Helper script for bundling up a game in a ZIP file.

This script will bundle all game files into a ZIP file which is named as
per the argument given on the command-line. The ZIP file will unpack into a
directory of the same name.

The script ignores:

- CVS or SVN subdirectories
- any dotfiles (files starting with ".")
- .pyc and .pyo files

'''

import sys
import os
import zipfile

if len(sys.argv) != 2:
    print '''Usage: python %s <release filename-version>

eg. python %s my_cool_game-1.0'''%(sys.argv[0], sys.argv[0])
    sys.exit()

base = sys.argv[1]

try:
    package = zipfile.ZipFile(base + '.zip', 'w', zipfile.ZIP_DEFLATED)
except RuntimeError:
    package = zipfile.ZipFile(base + '.zip', 'w')

# core files
for name in 'README.txt run_game.py'.split():
    package.write(name, os.path.join(base, name))
package.write('run_game.py', os.path.join(base, 'run_game.pyw'))

# utility for adding subdirectories
def add_files(generator):
    for dirpath, dirnames, filenames in generator:
        for name in 'CVS', '.svn':
            if name in dirnames:
                dirnames.remove(name)

        for name in filenames:
            suffix = os.path.splitext(name)[1]
            if suffix in ('.pyc', '.pyo'): continue
            if name[0] == '.': continue
            filename = os.path.join(dirpath, name)
            package.write(filename, os.path.join(base, filename))

# add the lib and data directories
add_files(os.walk('lib'))
add_files(os.walk('data'))
add_files(os.walk('eggs'))

