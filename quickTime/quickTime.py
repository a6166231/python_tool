#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import indexOf
from typeBtn.qtTypeBtnFact import createQTTypeBtnByType
from tkGUI import tk
import sys,os,json
import timeQuickJump

if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

os.chdir(absPath)

CFG_JSON_PATH = './cfg.json'

def SetJsonData():
    f = open(CFG_JSON_PATH,'w',encoding='utf-8')
    f.write(str(json.dumps(cfgJson,indent=4,ensure_ascii=False)))
    f.close()

if os.path.exists(CFG_JSON_PATH):
    f = open(os.path.join(CFG_JSON_PATH),'r',encoding='utf-8')
    cfgJson = json.loads(f.read())
    f.close()
else :
    cfgJson = {"data":{}}
    SetJsonData()


window = tk.createWindow(name='quickTime',width=490,height=440)
main = tk.createFrame(window)
main.pack(expand=True,fill='both')

leftFrame = tk.createFrame(main)
leftFrame.pack(side='left', fill='y',padx=10)
rightFrame = tk.createFrame(main)
rightFrame.pack(side='left', fill='y')

typeBtnsList = {
    '时间点': 'QTTimeTypeBtn',
    '相对时间': 'QTRelativeTimeTypeBtn',
    '星期': 'QTWeekDayTypeBtn',
    '月': 'QTMonthDayTypeBtn'
}
dateList = [[{'年':"year"},{'月':'month'},{'日':'day'}],[{'时':'hour'},{'分':'minute'},{'秒':'second'}]]

TOOL_NAME = '釫钶钛𬭁'


topMostTag = False
def createGMFrame():
    gmFrame = tk.createFrame(leftFrame)
    gmFrame.grid(row = 0, column = 0)
    gmFrame.config(width=150,height=200)

    def windowTopMost(tag:bool):
        global topMostTag
        topMostTag = tag
        window.attributes("-topmost", 1 if tag else 0)
        btnTop.config(foreground='green' if tag else 'black',relief= 'sunken' if tag else 'raised')

    def clearCfg():
        cfgJson["data"] = {}
        for k in map_qt_frame:
            map_qt_frame[k].clear()
        SetJsonData()

    def resetTime():
        from datetime import datetime
        import ntplib
        def get_network_time():
            NTP_SERVER = "time.windows.com"
            client = ntplib.NTPClient()
            response = client.request(NTP_SERVER)
            network_time = datetime.fromtimestamp(response.tx_time)
            return network_time
        _time = get_network_time()
        timeQuickJump.TimeQuickJump.updateSysTime(timeQuickJump.create_date_time(_time.year, _time.month, _time.day, _time.hour, _time.minute, _time.second))


    btnTop = tk.createBtn(gmFrame, '置顶', command=lambda:windowTopMost(not topMostTag))
    btnTop.place(x=0,y=10)
    btnTop = tk.createBtn(gmFrame, '重置', command=lambda:resetTime())
    btnTop.place(x=50,y=10)
    btnTop = tk.createBtn(gmFrame, '清理', command=lambda:clearCfg())
    btnTop.place(x=100,y=10)

    toolName = tk.createLb(gmFrame, TOOL_NAME)
    toolName.place(x=5, y=100)

    toolName.config(font=('kaiti',20,'bold'), fg='#ffa500')

def createTimeFrame():
    timeFrame = tk.createFrame(leftFrame)
    timeFrame.grid(row=1, column=0)
    timeFrame.config(width=150,height=200)

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
map_qt_frame = {}
def createCustomTimeBtns():
    titleFrame = tk.createFrame(rightFrame)
    titleFrame.grid(row=0, column=0, padx=5, pady=5)

    funBtnFrame = tk.createFrame(rightFrame)
    funBtnFrame.grid(row=1, column=0, padx=5, pady=5)

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
            qt = createQTTypeBtnByType(typeBtnsList[_type], funBtnFrame, lambda data: createTimeJumpPfbData(_type, data),getTimeJumpPfbData(_type))
            map_qt_frame[_type] = qt

        qt.frame.pack()
        last_frame = qt.frame

    changeBtnListByType()
    index = 0
    for btn in typeBtnsList:
        raidBtn = tk.createRadioBtn(titleFrame, radio_var, btn, lambda : changeBtnListByType())
        raidBtn.pack(side = 'left', padx=0)
        index+=1

createGMFrame()
createTimeFrame()
createCustomTimeBtns()

main.mainloop()