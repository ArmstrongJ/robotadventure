APP_NAME = 'PrintStarZero'


cfg = {
    'name':APP_NAME,
    'version':'1.0',
    'description':'',
    'author':'',
    'author_email':'',
    'url':'',
    
    'py2exe.target':'',
    'py2exe.icon':'icon.ico', #64x64
    'py2exe.binary':APP_NAME, #leave off the .exe, it will be added
    
    'py2app.target':'',
    'py2app.icon':'icon.icns', #128x128
    
    'cx_freeze.cmd':'~/src/cx_Freeze-3.0.3/FreezePython',
    'cx_freeze.target':'',
    'cx_freeze.binary':APP_NAME,
    }
    
# usage: python setup.py command
#
# sdist - build a source dist
# py2exe - build an exe
# py2app - build an app
# cx_freeze - build a linux binary (not implemented)
#
# the goods are placed in the dist dir for you to .zip up or whatever...

from distutils.core import setup, Extension
try:
    import py2exe
except:
    pass

import sys
import glob
import os
import shutil

try:
    cmd = sys.argv[1]
except IndexError:
    print 'Usage: setup.py py2exe|py2app|cx_freeze'
    raise SystemExit

# utility for adding subdirectories
def add_files(dest,generator):
    for dirpath, dirnames, filenames in generator:
        for name in 'CVS', '.svn':
            if name in dirnames:
                dirnames.remove(name)

        for name in filenames:
            if '~' in name: continue
            suffix = os.path.splitext(name)[1]
            if suffix in ('.pyc', '.pyo'): continue
            if name[0] == '.': continue
            filename = os.path.join(dirpath, name)
            dest.append(filename)

# define what is our data
data = []
add_files(data,os.walk('data'))
data.extend(glob.glob('*.txt'))
data.extend(glob.glob('LICENSE'))
# define what is our source
src = []
add_files(src,os.walk('lib'))
src.extend(glob.glob('*.py'))

# build the sdist target
if cmd == 'sdist':
    f = open("MANIFEST.in","w")
    for l in data: f.write("include "+l+"\n")
    for l in src: f.write("include "+l+"\n")
    f.close()
    
    setup(
        name=cfg['name'],
        version=cfg['version'],
        description=cfg['description'],
        author=cfg['author'],
        author_email=cfg['author_email'],
        url=cfg['url'],
        )

# build the py2exe target
if cmd in ('py2exe',):
    dist_dir = os.path.join('dist',cfg['py2exe.target'])
    data_dir = dist_dir
    
    src = 'run_game.py'
    dest = cfg['py2exe.binary']+'.py'
    shutil.copy(src,dest)
    
    setup(
        options={'py2exe':{
            'dist_dir':dist_dir,
            'dll_excludes':['_dotblas.pyd','_numpy.pyd']
            }},
        windows=[{
            'script':dest,
            'icon_resources':[(1,cfg['py2exe.icon'])],
            }],
        )

# build the py2app target
if cmd == 'py2app':
    dist_dir = os.path.join('dist',cfg['py2app.target']+'.app')
    data_dir = os.path.join(dist_dir,'Contents','Resources')
    from setuptools import setup

    src = 'run_game.py'
    dest = cfg['py2app.target']+'.py'
    shutil.copy(src,dest)

    APP = [dest]
    DATA_FILES = []
    OPTIONS = {'argv_emulation': True, 'iconfile':cfg['py2app.icon']}

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

# make the cx_freeze target
if cmd == 'cx_freeze':
    dist_dir = os.path.join('dist',cfg['cx_freeze.target'])
    data_dir = dist_dir
    os.system('%s --install-dir %s --target-name %s run_game.py'%(cfg['cx_freeze.cmd'],cfg['cx_freeze.binary'],dist_dir))

# recursively make a bunch of folders
def make_dirs(dname_):
    parts = list(os.path.split(dname_))
    dname = None
    while len(parts):
        if dname == None:
            dname = parts.pop(0)
        else:
            dname = os.path.join(dname,parts.pop(0))
        if not os.path.isdir(dname):
            os.mkdir(dname)

# copy data into the binaries 
if cmd in ('py2exe','cx_freeze','py2app'):
    dest = data_dir
    for fname in data:
        dname = os.path.join(dest,os.path.dirname(fname))
        make_dirs(dname)
        if not os.path.isdir(fname):
            shutil.copy(fname,dname)

