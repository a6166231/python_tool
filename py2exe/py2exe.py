#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import os,json,sys,shutil

if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

os.chdir(absPath)

def exit(showPause):
    if showPause:
        os.system('pause')
    os.system('exit')

try:
    ppath = sys.argv[1]
except:
    print('get args error :',sys.argv)
    exit(True)

pdir = os.path.dirname(ppath)
pname = os.path.basename(ppath).split('.')[0]

os.chdir(pdir)
status = os.system('pyinstaller -F ./%s.py' % pname)
if status == 0 and os.path.exists('./dist/%s.exe' % pname):
    shutil.copyfile('./dist/%s.exe' % (pname), './%s.exe' % (pname))
    shutil.rmtree('./dist')
    shutil.rmtree('./build')
    os.remove('./%s.spec' % (pname))