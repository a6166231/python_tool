from tkinter import Button, Entry
from typeBtn.qtTypeBtnBase import QTTypeBtnBase
import timeQuickJump
from tkGUI import tk

class QTRelativeTimeTypeBtn(QTTypeBtnBase):
    def __init__(self, frame, editStatus):
        self.type = timeQuickJump.TimePrefabType.RELATIVE_TIME.value
        super().__init__(frame, editStatus)

    # 生成自定义的按钮数据
    def getCustomBtnPrefabData(self):
        dayTag = self.day['tag']
        hourTag = self.hour['tag']
        minuteTag = self.minute['tag']
        if not dayTag and not hourTag and not minuteTag:
            return None

        dayData = self.day['data']
        hourData = self.hour['data']
        minuteData = self.minute['data']

        if dayData == 0 and hourData == 0 and minuteData == 0:
            print('?')
            return None

        sdata = '%s-%s-%s' % (dayData if dayTag else 0, hourData if hourTag else 0, minuteData if minuteTag else 0)
        return {
            # 'type': self.type,
            'data': sdata
        }

    def createCustomWidget(self, parent):
        funBtnFrame = tk.createLabelFrame(parent)

        btnData1 = { "tag": False , "name": "天", "data": 0}
        btnData2 = { "tag": False , "name": "小时", "data": 0}
        btnData3 = { "tag": False , "name": "分钟", "data": 0}

        self.day = btnData1
        self.hour = btnData2
        self.minute = btnData3

        def stautsBtnCheck(btn: Button, data):
            data['tag'] = not data['tag']
            tag = data['tag']
            tk.setBtnStyleStatus(btn, tag)

        def timeTrackUpdate(edit:Entry, data):
            # data["data"] = int(edit.get())
            try:
                data["data"] = int(edit.get())
            except:
                data["data"] = 0

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

        btnExport = tk.createBtn(funBtnFrame,'create', lambda: self.createCustomBtnPrefabData())
        btnExport.grid(row=0, column=4, padx=8, pady=5)

        return funBtnFrame

