
from timeQuickJump import TimeQuickJump, get_now_time
from tkGUI import tk

PFB_WIDTH = 280

class QTPrefabWidgetBase:
    def __init__(self, parent, data) -> None:
        self.data = data
        self.formatData()
        self.frame = self.createFrame(parent)
        self.frame.pack()
        self.editState = False
        self.setEditState(self.editState)

    def formatData(self):
        pass
    def getNow(self):
        return get_now_time()

    def setTime(self, time):
        TimeQuickJump.updateSysTime(time)

    def setEditState(self, state:bool):
        self.editState = state

        if not state:
            self.upBtn.pack_forget()
            self.delBtn.pack_forget()

            self.leftBtn.pack()
            self.setBtn.pack()
            self.rightBtn.pack()
        else:
            self.upBtn.pack()
            self.delBtn.pack()

            self.leftBtn.pack_forget()
            self.setBtn.pack_forget()
            self.rightBtn.pack_forget()

    def createFrame(self, parent):
        frame = tk.createFrame(parent)
        lbFrame = tk.createLabelFrame(frame)
        lbFrame.pack(fill='x')

        self.delBtn = tk.createBtn(lbFrame, '[X]')
        self.delBtn.pack(side='left')

        lbInfopar = tk.createFrame(lbFrame)
        self.lbInfo = tk.createLb(lbInfopar, self.getInfoName())
        self.lbInfo.pack()
        self.lbInfo.config(width=27, anchor='w')

        lbInfopar.pack(side='left',fill='x',expand=True)

        self.leftBtn = tk.createBtn(lbFrame, '<-', lambda: self.leftTime())
        self.leftBtn.pack(side='left')

        self.setBtn = tk.createBtn(lbFrame, '+', lambda: self.triggerTime())
        self.setBtn.pack(side='left')

        self.rightBtn = tk.createBtn(lbFrame, '->', lambda: self.rightTime())
        self.rightBtn.pack(side='left')

        self.upBtn = tk.createBtn(lbFrame, '^', lambda: self.moveIndex())
        self.upBtn.pack(side='left')

        lbFrame.config(width=PFB_WIDTH)
        return frame

    def getInfoName(self):
        return self.data["data"]
    def leftTime(self):
        return
    def rightTime(self):
        return
    def triggerTime(self):
        return

    def moveIndex(self):
        pass