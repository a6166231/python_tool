import datetime
from tkinter import BaseWidget, Button, Entry
from typing import Callable
import timeQuickJump
from tkGUI import tk

class QTWeekDayTypeBtn:
    def __init__(self, frame, createCall) -> None:
        self.frame = frame
        self.createCall = createCall
        self.dateData = {}
        self.timeData = {}
        self.type = timeQuickJump.TimePrefabType.TIME_ALL.value

    # 生成自定义的按钮数据
    def createCustomBtnPrefabData(self):
        pass
        # return self.createCall({
        #     'type': self.type,
        #     'data': sdata
        # })

    @staticmethod
    def create(parent:BaseWidget, createCall:Callable):
        frame = tk.createFrame(parent)
        qt = QTWeekDayTypeBtn(frame, createCall)

        customWidget = QTWeekDayTypeBtn.createCustomWidget(frame, qt)
        customWidget.grid(row=0,column=0)

        customBtnList = QTWeekDayTypeBtn.createCustomBtnList(frame, qt)
        customBtnList.grid(row=1,column=0,pady=5)

        return qt

    #自定义的时间点导出按钮
    @staticmethod
    def createCustomWidget(parent, qt):
        funBtnFrame = tk.createLabelFrame(parent)
        _time = datetime.datetime.now()

        btnData1 = { "tag": False , 'name': '天', "data": 0}
        btnData2 = { "tag": False , 'name': '小时', "data": 0}
        btnData3 = { "tag": False , 'name': '分钟', "data": 0}

        qt.day = btnData1
        qt.hour = btnData2
        qt.minute = btnData3

        def stautsBtnCheck(btn: Button, data):
            data['tag'] = not data['tag']
            tag = data['tag']
            btn.config(foreground='green' if tag else 'black', relief= 'sunken' if tag else 'raised')

        def timeTrackUpdate(edit:Entry, data, index):
            data[index] = int(edit.get())

        def createTimeTrackFrame(frameparent, data):
            trackFrame = tk.createFrame(frameparent)

            btn = tk.createBtn(funBtnFrame, data.name, lambda : stautsBtnCheck(btn, data))
            stautsBtnCheck(btn, data)

            edit1 = tk.createEdit(trackFrame, data['data'][0], lambda: timeTrackUpdate(edit1, data["data"], 0))
            edit1.config(width=4)

            btn.grid(row=0, column=0, padx=1)
            edit1.grid(row=0, column=1, padx=1)

            return trackFrame

        # checkBox1 = tk.createBtn(funBtnFrame, '天', lambda : stautsBtnCheck(checkBox1, btnData1))
        # checkBox2 = tk.createBtn(funBtnFrame, '小时', lambda : stautsBtnCheck(checkBox2, btnData2))
        # checkBox3 = tk.createBtn(funBtnFrame, '分钟', lambda : stautsBtnCheck(checkBox3, btnData3))

        # stautsBtnCheck(checkBox1, btnData1)
        # stautsBtnCheck(checkBox2, btnData2)
        # stautsBtnCheck(checkBox3, btnData3)

        # checkBox1.grid(row=0, column=1, pady=5, padx=5)
        # checkBox2.grid(row=0, column=2, pady=5, padx=5)
        # checkBox3.grid(row=0, column=3, pady=5, padx=5)

        timetrack1 = createTimeTrackFrame(funBtnFrame, btnData1)
        timetrack2 = createTimeTrackFrame(funBtnFrame, btnData2)
        timetrack3 = createTimeTrackFrame(funBtnFrame, btnData2)
        timetrack1.grid(row=0, column=1, padx=12, pady=5)
        timetrack2.grid(row=0, column=2, padx=12, pady=5)
        timetrack3.grid(row=0, column=3, padx=12, pady=5)

        btnExport = tk.createBtn(funBtnFrame,'create', lambda: qt.createCustomBtnPrefabData())
        btnExport.grid(row=0, column=3, padx=12, pady=5, rowspan=2)

        funBtnFrame.config(width=300,height=50)
        return funBtnFrame

    #自定义的时间点按钮列表
    @staticmethod
    def createCustomBtnList(parent, qt):
        funBtnFrame = tk.createLabelFrame(parent)
        funBtnFrame.config(width=300,height=300)

        return funBtnFrame
