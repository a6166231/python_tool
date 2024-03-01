from tkinter import Entry
from tkGUI import tk
from typeBtn.qtTypeBtnBase import QTTypeBtnBase
import timeQuickJump

class QTMonthDayTypeBtn(QTTypeBtnBase):
    def __init__(self, frame, editStatus):
        self.type = timeQuickJump.TimePrefabType.MONTH_DAY.value
        super().__init__(frame, editStatus)

    # 生成自定义的按钮数据
    def getCustomBtnPrefabData(self):
        if self.monthDay <= 0 or self.monthDay > 31:
            print("?")
            return None
        return {
            # 'type': self.type,
            'data': self.monthDay
        }

    def createCustomWidget(self, parent):
        funBtnFrame = tk.createLabelFrame(parent)

        self.monthDay = 1

        def timeTrackUpdate(edit:Entry):
            try:
                self.monthDay = int(edit.get())
            except:
                self.monthDay = 1

        trackFrame = tk.createFrame(funBtnFrame)
        trackFrame.pack(fill="both", expand=True)

        edit1 = tk.createEdit(trackFrame, str(self.monthDay), lambda: timeTrackUpdate(edit1))
        edit1.grid(row=0, column=0, padx=30)
        edit1.config(width=10)
        lb = tk.createLb(trackFrame, '号')
        lb.grid(row=0, column=1, padx=2)

        btnExport = tk.createBtn(trackFrame,'create', lambda: self.createCustomBtnPrefabData())
        btnExport.grid(row=0, column=2, padx=50, pady=5)

        # trackFrame.config(width=300)

        return funBtnFrame