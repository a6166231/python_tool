#!/usr/bin/python
#-*- coding: utf-8 -*-

import json, os, colorama
from colorama import Fore

colorama.init(autoreset=True)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SPINE_COMPLETE_EVENT_NAME = "end_point1"
SPINE_EVENT_START_NAME = "_start"
SPINE_EVENT_END_NAME = "_end"

LEVEL_1 = '  - '
LEVEL_2 = '    - '

IMG_MAX_SIZE = [2048, 2048]

# 检测所有动画
def checkAnimation(animations, vSlot, vBone, vAtt):
    vAnimation = []
    if len(animations) == 0:
        return []
    for ani in animations:
        vAnimation.append(ani)
        vAniAttFrame = checkAnimationAttFrame(animations, ani)
        print(LEVEL_1 + u'动画名: ' + Fore.GREEN + ani + Fore.RESET )
        vReadyEventSlot = []
        vReadyEventBone = []
        vUnReadyEvent = []
        try:
            vReadyEventSlot,vReadyEventBone,vUnReadyEvent = checkAllEvent(animations[ani]["events"], vSlot, vBone)
        except:
            pass
        vSameAttFrame = set(vAtt) & set(vAniAttFrame)
        if  len(vReadyEventSlot) == 0 and len(vReadyEventBone) == 0 and len(vSameAttFrame) == 0 and len(vUnReadyEvent) == 0:
            continue

        if len(vUnReadyEvent):
            print(LEVEL_2 + u'普通事件: '+ Fore.LIGHTWHITE_EX +'[' + ", ".join(vUnReadyEvent) + ']'+ Fore.RESET)
        if len(vReadyEventSlot):
            print(LEVEL_2 + u'可跟随的【插槽】事件: '+ Fore.CYAN +'[' + ", ".join(vReadyEventSlot) + ']'+ Fore.RESET)
        if len(vReadyEventBone):
            print(LEVEL_2 + u'可跟随的【骨骼】事件: '+ Fore.CYAN +'[' + ", ".join(vReadyEventBone) + ']'+ Fore.RESET)
        if len(vSameAttFrame):
            print(LEVEL_2 + u'影响替换插槽的附件帧: '+ Fore.RED +'[' + ", ".join(vSameAttFrame) + ']'+ Fore.RESET)

# 所有的动画事件
def checkAnimationEvent(events):
    vEvent = []
    try:
        for event in events:
            vEvent.append(event["name"])
    except:
        pass
    vEvent.sort()
    return vEvent

# 检测动画里的所有的附件帧
def checkAnimationAttFrame(animations,ani):
    vAniAttFrame = []
    try:
        for bone in animations[ani]["slots"]:
            try:
                if len(animations[ani]["slots"][bone]["attachment"]):
                    vAniAttFrame.append(bone)
            except:
                continue
    except:
        pass
    vAniAttFrame.sort()
    return vAniAttFrame

# 检测所有插槽
def checkSlots(slots):
    vAtt = []
    vSlot = {}
    if len(slots) == 0:
        return vAtt

    # 根据json文件的blend变化次数来计算dc
    # 动效对骨骼的 隐藏/显示 会影响实际运行的dc   
    # 只是做一个参考  
    bakBlend = '-1'
    dc = 1
    for slot in slots:
        vSlot[slot["name"]] = slot
        try:
            if slot["attachment"]:
                vAtt.append(slot["name"])
        except:
            pass

        try:
            blend = slot["blend"]
        except:
            blend = ''

        if bakBlend == '-1':
            bakBlend = blend
        elif blend != bakBlend:
            bakBlend = blend
            dc+=1
    vAtt.sort()
    return vAtt,vSlot,dc

# 检测所有骨骼
def checkBones(bones):
    vBones = {}
    if len(bones) == 0:
        return vBones
    for bone in bones:
        try:
            vBones[bone["name"]] = bone
        except:
            continue
    return vBones

#检测fallow是否合规
def checkAllEvent(vAniEvent, vSlot, vBone):
    unReadyEvent = []
    map = {}
    for event in vAniEvent:
        sEvent = event['name']
        unReadyEvent.append(sEvent)
        if sEvent.endswith(SPINE_EVENT_START_NAME) or sEvent.endswith(SPINE_EVENT_END_NAME):
            index = endsIndex(sEvent,SPINE_EVENT_START_NAME) 
            index = index if index >= 0 else endsIndex(sEvent,SPINE_EVENT_END_NAME)
            sname = sEvent[0:index]
            eData = map.get(sname)
            
            if not eData:
                eData = {}
            if sname + SPINE_EVENT_START_NAME == sEvent:
                eData['start'] = eData['start'] + 1 if eData.get('start') else 1
            if sname + SPINE_EVENT_END_NAME == sEvent:
                eData['end'] = eData['end'] + 1 if eData.get('end') else 1
            map[sname] = eData
            
    readyEventSlot = []
    readyEventBone = []
    for sPrefix in map:
        obj = map.get(sPrefix)
        try :
            if obj:
                # 事件中存在 xxx_start和xxx_end 且 只出现了一次
                if obj['start'] == obj['end'] and obj['start'] == 1:
                    # if vSlot.get(sPrefix) and vBone.get(sPrefix):
                    # 只判断插槽、骨骼是否存在即可  动效的骨骼和插槽名可能会不一样
                    if vSlot.get(sPrefix):
                        readyEventSlot.append(sPrefix)
                        unReadyEvent.remove(sPrefix+'_start')
                        unReadyEvent.remove(sPrefix+'_end')
                    elif vBone.get(sPrefix):
                        readyEventBone.append(sPrefix)
                        unReadyEvent.remove(sPrefix+'_start')
                        unReadyEvent.remove(sPrefix+'_end')
                    else:
                        print(LEVEL_2 + Fore.RED + u'事件【' + sPrefix + u'_start/end】符合规则，但不存在插槽/骨骼名叫 【' + sPrefix + u'】'+ Fore.RESET)
                else:
                    print(LEVEL_2 + Fore.RED + u'事件【xxx_start/end】出现多次'+ Fore.RESET)

        except :
            pass
    readyEventSlot.sort()
    readyEventBone.sort()
    unReadyEvent.sort()
    return readyEventSlot,readyEventBone, unReadyEvent

# 是否以字符串s为结尾的
def endsIndex(s, sub):
    index = -1
    if len(sub) > len(s):
        return index
    subindex = 0
    for i in range(len(s) - len(sub), len(s)):
        if(s[i] != sub[subindex]):
            return index
        subindex+=1
    return len(s) - len(sub)

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

        pngsStr = LEVEL_1 + u'图集尺寸: '
        for png in pngObj:
            size = pngObj[png]['size'].split(',')
            tipcolor = Fore.GREEN
            if int(size[0]) > IMG_MAX_SIZE[0] or int(size[0]) > IMG_MAX_SIZE[1]:
                tipcolor = Fore.RED
            pngsStr += tipcolor + '(' + size[0] + ',' + size[1] + ')    ' + Fore.RESET
        return pngsStr
    except:
        return False
# 检测json文件
def checkJson(root,file):
    fpath = os.path.join(root,file)
    fs = open(fpath, 'r')
    succ = False
    try:
        obj = json.loads(fs.read())
        sk = obj["skeleton"]
        pngStr = checkTexure(root,file)
        if not pngStr:
            return False
        print(fpath)
        print(pngStr)
        vAtt,vSlot,dc = checkSlots(obj["slots"])
        vBone = checkBones(obj["bones"])
        
        dcColor = Fore.GREEN if dc <= 4 else Fore.RED
        print(LEVEL_1 + u"dc: "  + dcColor + str(dc) + Fore.RESET)
        if len(vAtt):
            print(LEVEL_1 + u"可替换插槽的名: " + Fore.GREEN +  "[" + ", ".join(vAtt) + ']' + Fore.RESET)
        checkAnimation(obj["animations"], vSlot, vBone, vAtt)
        print('\n')
        succ = True
    except:
        print(Fore.RED + fpath + ' is not a spine file.' + Fore.RESET)
        print('\n')

    fs.close()
    return succ

total = 0
for root,dirs,files in os.walk('.'):
    for file in files:
        if file.endswith(".json"):
            if checkJson(root,file):
                total+=1
print("total spine number: " + Fore.GREEN + str(total) + Fore.RESET)
os.system('pause')