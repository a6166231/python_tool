import datetime
from tkinter import Button, Entry
import timeQuickJump
from tkGUI import tk
from typeBtn.qtTypeBtnBase import QTTypeBtnBase

class QTTimeTypeBtn(QTTypeBtnBase):
    def __init__(self, frame, createCall, pfbData) -> None:
        super().__init__(frame, createCall, pfbData)
        self.type = timeQuickJump.TimePrefabType.TIME_ALL.value

    # 生成自定义的按钮数据
    def getCustomBtnPrefabData(self):
        sdata = ''
        dateTag = self.dateData['tag']
        timeTag = self.timeData['tag']
        dateData = self.dateData['data']
        timeData = self.timeData['data']
        if dateTag:
            sdata += '%s-%s-%s' % (dateData[0],dateData[1],dateData[2])

        if timeTag:
            if dateTag:
                sdata += ' '
            sdata += '%s:%s:%s' % (timeData[0],timeData[1],timeData[2])

        return {
            'type': self.type,
            'data': sdata
        }

    #自定义的时间点导出按钮
    def createCustomWidget(self, parent):
        funBtnFrame = tk.createLabelFrame(parent)
        _time = datetime.datetime.now()

        btnData1 = { "tag": False , "data": [_time.year, _time.month, _time.day]}
        btnData2 = { "tag": False , "data": [_time.hour, _time.minute, _time.second]}

        self.dateData = btnData1
        self.timeData = btnData2

        def stautsBtnCheck(btn: Button, data):
            data['tag'] = not data['tag']
            tag = data['tag']
            btn.config(foreground='green' if tag else 'black', relief= 'sunken' if tag else 'raised')

        def timeTrackUpdate(edit:Entry, data, index):
            # data[index] = int(edit.get())
            try:
                data[index] = int(edit.get())
            except:
                data[index] = 0

        def createTimeTrackFrame(frameparent, data, gap):
            trackFrame = tk.createFrame(frameparent)

            edit1 = tk.createEdit(trackFrame, data['data'][0], lambda: timeTrackUpdate(edit1, data["data"], 0))
            edit2 = tk.createEdit(trackFrame, data['data'][1], lambda: timeTrackUpdate(edit2, data["data"], 1))
            edit3 = tk.createEdit(trackFrame, data['data'][2], lambda: timeTrackUpdate(edit3, data["data"], 2))

            edit1.config(width=4)
            edit2.config(width=4)
            edit3.config(width=4)

            line1 = tk.createLb(trackFrame, gap, 12)
            line2 = tk.createLb(trackFrame, gap, 12)

            edit1.grid(row=0, column=0, pady=1)
            line1.grid(row=0, column=1, pady=1)
            edit2.grid(row=0, column=2, pady=1)
            line2.grid(row=0, column=3, pady=1)
            edit3.grid(row=0, column=4, pady=1)

            return trackFrame

        checkBox1 = tk.createBtn(funBtnFrame, '年月日', lambda : stautsBtnCheck(checkBox1, btnData1))
        checkBox2 = tk.createBtn(funBtnFrame, '时分秒', lambda : stautsBtnCheck(checkBox2, btnData2))

        stautsBtnCheck(checkBox1, btnData1)
        stautsBtnCheck(checkBox2, btnData2)

        checkBox1.grid(row=0, column=0, pady=5, padx=15)
        checkBox2.grid(row=1, column=0, pady=5, padx=15)

        timetrack1 = createTimeTrackFrame(funBtnFrame, btnData1, '-')
        timetrack2 = createTimeTrackFrame(funBtnFrame, btnData2, ':')
        timetrack1.grid(row=0, column=1, padx=12, pady=5)
        timetrack2.grid(row=1, column=1, padx=12, pady=5)

        btnExport = tk.createBtn(funBtnFrame,'create', lambda: self.createCustomBtnPrefabData())
        btnExport.grid(row=0, column=3, padx=12, pady=5, rowspan=2)

        funBtnFrame.config(width=300,height=50)
        return funBtnFrame