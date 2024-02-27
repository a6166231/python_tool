#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import indexOf
from tkGUI import tk
import sys,os,json
import timeQuickJump
import typeBtn.qtTimeTypeBtn as qtTimeTypeBtn
import typeBtn.qtMonthDayTypeBtn as qtMonthDayTypeBtn
import typeBtn.qtRelativeTimeTypeBtn as qtRelativeTimeTypeBtn
import typeBtn.qtWeekDayTypeBtn as qtWeekDayTypeBtn


if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

os.chdir(absPath)


f = open(os.path.join('./cfg.json'),'r',encoding='utf-8')
cfgJson = json.loads(f.read())
f.close()

window = tk.createWindow(name='quickTime',width=530,height=420)
main = tk.createFrame(window)
main.pack(expand=True,fill='both')
topFrame = tk.createFrame(main)
topFrame.grid(row=0, column=0, padx=10, pady=10,columnspan=2)

# btnTop = tk.createBtn(topFrame, '置顶', command=lambda:windowTopMost(not topMostTag))
# btnTop.pack(side='right', padx=0)

leftFrame = tk.createFrame(main)
leftFrame.grid(row=1, column=0, padx=10, pady=10)
rightFrame = tk.createFrame(main)
rightFrame.grid(row=1, column=1, padx=10, pady=10)

topMostTag = False

typeBtnsList = {
    '时间点': qtTimeTypeBtn.QTTimeTypeBtn,
    '相对时间': qtRelativeTimeTypeBtn.QTRelativeTimeTypeBtn,
    '星期': qtWeekDayTypeBtn.QTWeekDayTypeBtn,
    '月': qtMonthDayTypeBtn.QTMonthDayTypeBtn
}
dateList = [[{'年':"year"},{'月':'month'},{'日':'day'}],[{'时':'hour'},{'分':'minute'},{'秒':'second'}]]

# def windowTopMost(tag:bool):
#     global topMostTag
#     topMostTag = tag
#     window.attributes("-topmost", 1 if tag else 0)
#     btnTop.config(foreground='green' if tag else 'black',relief= 'sunken' if tag else 'raised')

def SetJsonData():
    f = open('./cfg.json','w',encoding='utf-8')
    f.write(str(json.dumps(cfgJson,indent=4,ensure_ascii=False)))
    f.close()

def createTimeFrame():
    timeFrame = tk.createFrame(leftFrame)
    timeFrame.pack(fill='both')

    now = timeQuickJump.get_now_time()
    editMap = {}

    def editCall(dateIndex,v):
        try:
            editMap[dateIndex] = int(v)
        except:
            editMap[dateIndex] = 0

    def createEditInput(frame, title: str, value:str, dateIndex):
        lbEdit = tk.createEdit(frame, str(now.__getattribute__(value)), lambda : editCall(dateIndex, lbEdit.get()))
        lbName = tk.createLb(frame, title)
        lbEdit.config(width=4)
        lbEdit.pack(side = 'left', pady = 15)
        lbName.pack(side = 'left', pady = 15)

        frame.pack()
        return int(now.__getattribute__(value))

    dateIndex = 0
    for time_track in dateList:
        frame = tk.createFrame(timeFrame)
        index = 0
        for _data in time_track:
            key = list(_data.keys())[0]
            editCall(dateIndex, createEditInput(frame, key, _data[key], dateIndex))
            index += 1
            dateIndex += 1

    def setEditTime():
        timeQuickJump.TimeQuickJump.updateSysTime(timeQuickJump.create_date_time(editMap[0], editMap[1], editMap[2], editMap[3], editMap[4], editMap[5]))

    btn = tk.createBtn(timeFrame, 'update', command=lambda :setEditTime())
    btn.pack(fill='x',pady=20)

def createCustomBtnPrefab(parent, btnData, command:str = ''):
    frame = tk.createFrame(parent)
    btn = tk.createBtn(frame, "", command)
    btn.pack(fill='x',pady=20)

def createTimeJumpPfbData(_type, data):
    pfbData = getTimeJumpPfbData(_type)
    pfbData.append(data)
    SetJsonData()

def getTimeJumpPfbData(_type):
    key = str(indexOf(typeBtnsList, _type))
    typeData = cfgJson["data"].get(key)
    if not typeData:
        typeData = {}
        cfgJson["data"][key] = typeData

    pfbData = typeData.get('pfbData')
    if not pfbData:
        pfbData = []
        typeData['pfbData'] = pfbData
        SetJsonData()
    return pfbData

def createCustomTimeBtns():
    titleFrame = tk.createFrame(rightFrame)
    titleFrame.grid(row=0, column=0, padx=5, pady=5)

    funBtnFrame = tk.createFrame(rightFrame)
    funBtnFrame.grid(row=1, column=0, padx=5, pady=5)

    map_qt_frame = {}
    radio_var = tk.StringVar(value=list(typeBtnsList.keys())[0])
    global last_frame
    last_frame = None

    def changeBtnListByType():
        global last_frame
        if last_frame:
            last_frame.pack_forget()

        _type = radio_var.get()
        try:
            qt = map_qt_frame[_type]
        except:
            qt = typeBtnsList[_type].create(funBtnFrame, lambda data: createTimeJumpPfbData(_type, data),getTimeJumpPfbData(_type))
            map_qt_frame[_type] = qt
        qt.frame.pack()
        last_frame = qt.frame

    changeBtnListByType()
    index = 0
    for btn in typeBtnsList:
        raidBtn = tk.createRadioBtn(titleFrame, radio_var, btn, lambda : changeBtnListByType())
        raidBtn.pack(side = 'left', padx=0)
        index+=1

createTimeFrame()
createCustomTimeBtns()

main.mainloop()