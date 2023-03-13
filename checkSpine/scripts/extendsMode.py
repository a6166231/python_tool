#!/usr/bin/python
#-*- coding: utf-8 -*-
import webbrowser
import json, os, colorama,sys
# from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf-8')
colorama.init(autoreset=True)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

EXTENDS_TAR_STR = 'window.extendsMode'

batPath = os.path.join(os.path.dirname(sys.argv[0]),'index.html')
f = open(batPath,'r+')
flist=f.readlines()
f.close()
f = open(batPath,'w+')
lines = 0
for line in flist:
    try:
        index = line.index(EXTENDS_TAR_STR)
        if index != -1:
            print(lines)
            # flist[178] = EXTENDS_TAR_STR + '=' + json.dumps(cfg)+'\n'
            break
    except:
        pass
    lines = lines + 1
f.writelines(flist)
f.close()
webbrowser.open(batPath)