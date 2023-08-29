#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,json,sys,datetime
from enum import Enum
from utils.utils import *
from cc import *

if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

os.chdir(absPath)

sPfbExtendsName = '.prefab'

sTransition = '_transition'
sNormalrSpf = '_normalSprite'
sPressSpf = '_pressedSprite'
sDisableSpf = '_disabledSprite'
class TRANSITION(Enum):
    NONE = 0
    COLOR = 1
    SPRITE = 2
    SCALE = 3

f = open(os.path.join('./cfg.json'),'r',encoding='utf-8')
cfgJson = json.loads(f.read())
f.close()

PPATH = cfgJson['ppath']
OPATH = cfgJson['out_path']
IGNORE_MAP = cfgJson['ignorePfb']

result = findFileBySuffixName(PPATH, sPfbExtendsName)

vExchangePfb = []
vReadyPfb = []

def formatBigFloat(val):
    if (len(str(val)) >= 23):
        return str(val)
    return float(val)

total = 0
for pfbPath in result: 
    f = open(pfbPath,'r',encoding='utf-8')
    fileName = os.path.basename(pfbPath).replace(sPfbExtendsName, '')
    mapIgnore = []
    try:
        mapIgnore = IGNORE_MAP[fileName]
    except:
        pass

    cfgJson = json.loads(f.read(),parse_float=formatBigFloat)
    f.close()

    pfb = Prefab()
    pfb.initPfbData(cfgJson)
    vButtons = pfb.getRootNode().getComponentsInChildren(Button)
    for i in range(len(vButtons)):
        item = vButtons[i]
        if item.data == None:
            continue
        # transition为spf类型 && press属性为空 && normal属性不空 && disable为空 就改为scale类型
        if (item.data[sTransition] == TRANSITION.SPRITE.value and item.data[sPressSpf] == None):
            nodeName = item.node.name
            index = -1
            try:
                index = mapIgnore.index(nodeName)
            except:
                pass
            if index >= 0:
                continue

            # disable不为空
            if (item.data[sDisableSpf] != None):
                vReadyPfb.append({
                    "path": pfbPath,
                    "fileName": fileName,
                    "name": nodeName,
                })
                continue
            # normal不为空
            if (item.data[sNormalrSpf] != None):
                total+=1
                vExchangePfb.append({
                    "path": pfbPath,
                    "fileName": fileName,
                    "name": nodeName,
                })
                print('【 %s 】: %s ' % (fileName, nodeName))
                cfgJson[item.id][sTransition] = TRANSITION.SCALE.value
                f = open(pfbPath,'w',encoding='utf-8')
                f.write(str(json.dumps(cfgJson,indent=2,ensure_ascii=False,default=formatBigFloat)))
                f.close()

try:
    os.makedirs(OPATH)
except:
    pass
sReadyPfb = ""
for item in vReadyPfb:
    sReadyPfb += item["fileName"] + ' : ' + item["name"] + '\n'

sExchangePfb = ""
for item in vExchangePfb:
    sExchangePfb += item["fileName"] + ' : ' + item["name"] + '\n'

# print('===============')
# print(sReadyPfb)
# print('----------------')
# print(sExchangePfb)
# print('===============')

data = datetime.datetime.now()
st = str(int(data.timestamp()))
sdata = str(data.year) + '_' + str(data.month) + '_' + str(data.day)

if len(sExchangePfb) > 0:
    f = open(os.path.join(OPATH, 'log_change_' + sdata + '_' + st + '.txt'),'w',encoding='utf-8')
    f.write(sExchangePfb)
    f.close()

if len(sReadyPfb) > 0:
    f = open(os.path.join(OPATH, 'log_ready_' + sdata + '_' + st + '.txt'),'w',encoding='utf-8')
    f.write(sReadyPfb)
    f.close()
print('total : ', total)
print('~~over~~')
os.system('pause')