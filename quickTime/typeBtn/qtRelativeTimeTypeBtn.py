from tkinter import BaseWidget, Button, Entry
from typing import Callable
from typeBtn.qtTypeBtnBase import QTTypeBtnBase
import timeQuickJump
from tkGUI import tk

class QTRelativeTimeTypeBtn(QTTypeBtnBase):
    def __init__(self, frame, createCall, pfbData):
        super().__init__(frame, createCall, pfbData)
        self.day = {}
        self.hour = {}
        self.minute = {}
        self.type = timeQuickJump.TimePrefabType.RELATIVE_TIME.value

    # 生成自定义的按钮数据
    def createCustomBtnPrefabData(self):
        dayTag = self.day['tag']
        hourTag = self.hour['tag']
        minuteTag = self.minute['tag']

        dayData = self.day['data']
        hourData = self.hour['data']
        minuteData = self.minute['data']

        sdata = '%s-%s-%s' % (dayData if dayTag else 0, hourData if hourTag else 0, minuteData if minuteTag else 0)
        return self.createCall({
            'type': self.type,
            'data': sdata
        })

    @staticmethod
    def create(parent:BaseWidget, createCall:Callable, pfbData):
        frame = tk.createFrame(parent)
        qt = QTRelativeTimeTypeBtn(frame, createCall, pfbData)

        customWidget = QTRelativeTimeTypeBtn.createCustomWidget(frame, qt)
        customWidget.grid(row=0,column=0)

        customBtnList = QTTypeBtnBase.createCustomBtnList(frame, qt)
        customBtnList.grid(row=1,column=0,pady=5)

        return qt

    #自定义的时间点导出按钮
    @staticmethod
    def createCustomWidget(parent, qt):
        funBtnFrame = tk.createLabelFrame(parent)

        btnData1 = { "tag": False , "name": "天", "data": 0}
        btnData2 = { "tag": False , "name": "小时", "data": 0}
        btnData3 = { "tag": False , "name": "分钟", "data": 0}

        qt.day = btnData1
        qt.hour = btnData2
        qt.minute = btnData3

        def stautsBtnCheck(btn: Button, data):
            data['tag'] = not data['tag']
            tag = data['tag']
            btn.config(foreground='green' if tag else 'black', relief= 'sunken' if tag else 'raised')

        def timeTrackUpdate(edit:Entry, data):
            data["data"] = int(edit.get())

        def createTimeTrackFrame(frameparent, data):
            trackFrame = tk.createFrame(frameparent)

            btn = tk.createBtn(trackFrame, data["name"], lambda : stautsBtnCheck(btn, data))
            stautsBtnCheck(btn, data)

            edit1 = tk.createEdit(trackFrame, data['data'], lambda: timeTrackUpdate(edit1, data))
            btn.grid(row=0, column=0, padx=2)
            edit1.grid(row=0, column=1, padx=2)
            edit1.config(width=4)
            return trackFrame

        timetrack1 = createTimeTrackFrame(funBtnFrame, btnData1)
        timetrack2 = createTimeTrackFrame(funBtnFrame, btnData2)
        timetrack3 = createTimeTrackFrame(funBtnFrame, btnData3)
        timetrack1.grid(row=0, column=1, padx=3, pady=5)
        timetrack2.grid(row=0, column=2, padx=3, pady=5)
        timetrack3.grid(row=0, column=3, padx=3, pady=5)

        btnExport = tk.createBtn(funBtnFrame,'create', lambda: qt.createCustomBtnPrefabData())
        btnExport.grid(row=0, column=4, padx=8, pady=5)

        funBtnFrame.config(width=300,height=50)
        return funBtnFrame

