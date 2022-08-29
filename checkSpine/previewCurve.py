#!/usr/bin/python
#-*- coding: utf-8 -*-
import re
import webbrowser
import json, os, colorama,sys,subprocess
from colorama import Fore
from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf-8')
colorama.init(autoreset=True)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

bIsDir = True
sFilePath = ''
try:
    sFilePath = sys.argv[1]
    bIsDir = False
except:
    pass


def replaceStr(str):
    return str.replace("\n","").replace("\r","")
# 检测图片
def checkTexure(root,file):
    try :
        pname = os.path.splitext(file)[0]
        atlas = open(os.path.join(root ,pname + '.atlas'))
        pngObj = {}
        nowPng = ''
        for line in atlas.readlines():
            try:
                if line.index('.png') > -1:
                    nowPng = line
                    pngObj[nowPng] = {}
                    pngObj[nowPng]["png"] = replaceStr(line)
                    continue
            except:
                pass
            try:
                index = line.index('size: ')
                if pngObj[nowPng] and index > -1 :
                    pngObj[nowPng]['size'] = replaceStr(line)[index + 6:]
            except:
                nowPng = ''
        return pngObj
    except:
        return False

# 检测json文件
def checkJson(cfg,root,file):
    fpath = os.path.join(root,file)
    fs = open(fpath, 'r')
    succ = False

    try:
        pname = os.path.splitext(file)[0]
        obj = json.loads(fs.read())
        sk = obj["skeleton"]
        cfg[pname] = {}
        cfg[pname]['atlas'] = os.path.join(root,pname+'.atlas').decode('gbk')
        cfg[pname]['json'] = os.path.join(root,pname+'.json').decode('gbk')
        cfg[pname]['png'] = []
        pngStr = checkTexure(root,file)
        for key in pngStr:
            cfg[pname]['png'].append(os.path.join(root,key).decode('gbk'))
        if not pngStr:
            return False
        succ = True
    except:
        pass
    fs.close()
    return succ
cfg = {}
checkJson(cfg,os.path.dirname(sFilePath),os.path.basename(sFilePath))

import base64
for spine in cfg:
    print(cfg[spine]['atlas'])
    print(cfg[spine]['json'])
    print(cfg[spine]['png'])
    f = open(cfg[spine]['atlas'],'rb')
    print(base64.b64encode(f.read()))
    f.close()
# batPath = os.path.join(os.path.dirname(sys.argv[0]),'index.html')
# f = open(batPath,'r+')
# flist=f.readlines()
# f=open(batPath,'w+')
# flist[174]=u'<script>window.previewSpinePath='+json.dumps(cfg,ensure_ascii=False)+'</script>\n'
# f.writelines(flist)
# f.close()
# webbrowser.open(batPath)