#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys,shutil
absPath=''
if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

os.chdir(absPath)

def exit(showPause):
    if showPause:
        os.system('pause')
    os.system('exit')
ppath=''
try:
    ppath = sys.argv[1]
except:
    print('get args error :',sys.argv)
    exit(True)

pdir = os.path.dirname(ppath)
pname = os.path.basename(ppath).split('.')[0]

_w = input(' -w : 是否显示窗口参数(y/n):') or 'y'
_w = ' -w' if _w.lower() == 'n' else ''
os.chdir(pdir)

try:
    status = os.system('pyinstaller -F ./%s.py%s' % (pname, _w))
except Exception as err:
    print('py2exe err :', err)
    exit(True)

if status == 0 and os.path.exists('./dist/%s.exe' % pname):
    shutil.copyfile('./dist/%s.exe' % (pname), './%s.exe' % (pname))
    shutil.rmtree('./dist')
    shutil.rmtree('./build')
    os.remove('./%s.spec' % (pname))