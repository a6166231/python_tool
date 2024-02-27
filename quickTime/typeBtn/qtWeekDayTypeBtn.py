from tkinter import Entry
import timeQuickJump
from tkGUI import tk
from typeBtn.qtTypeBtnBase import QTTypeBtnBase

class QTWeekDayTypeBtn(QTTypeBtnBase):
    def __init__(self, frame, createCall, pfbData):
        super().__init__(frame, createCall, pfbData)
        self.type = timeQuickJump.TimePrefabType.WEEK_DAY.value

    # 生成自定义的按钮数据
    def getCustomBtnPrefabData(self):
        return {
            'type': self.type,
            'data': self.weekDay
        }

    def createCustomWidget(self, parent):
        funBtnFrame = tk.createLabelFrame(parent)

        self.weekDay = 1

        def timeTrackUpdate(edit:Entry):
            try:
                self.weekDay = int(edit.get())
            except:
                self.weekDay = 1

        trackFrame = tk.createFrame(funBtnFrame)
        trackFrame.pack(fill="both", expand=True)

        lb = tk.createLb(trackFrame, '周')
        edit1 = tk.createEdit(trackFrame, str(self.weekDay), lambda: timeTrackUpdate(edit1))
        lb.grid(row=0, column=0, padx=30)
        edit1.grid(row=0, column=1, padx=2)
        edit1.config(width=10)

        btnExport = tk.createBtn(trackFrame,'create', lambda: self.createCustomBtnPrefabData())
        btnExport.grid(row=0, column=2, padx=50, pady=5)

        # trackFrame.config(width=300)

        return funBtnFrame
