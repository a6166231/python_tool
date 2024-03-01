
from quickData import setTimeJumpPfbDatIndex
from timeQuickJump import TimeQuickJump, get_now_time
from tkGUI import tk

PFB_WIDTH = 280

class QTPrefabWidgetBase:
    editState:bool = False
    def __init__(self, parent, data ,qtType) -> None:
        self.data = data
        self.formatData()
        self.frame = self.createFrame(parent)
        self.editState = qtType.editState
        self.qtType = qtType
        self.setEditState(self.editState)

    def getAllBtnList(self):
        return [self.leftBtn, self.setBtn, self.rightBtn]
    def getVisibleBtnList(self):
        return self.getAllBtnList()
    def formatData(self):
        pass

    def getNow(self):
        return get_now_time()

    def setTime(self, time):
        TimeQuickJump.updateSysTime(time)

    def setEditState(self, state:bool):
        self.editState = state

        vbtnList = self.getVisibleBtnList()
        vAllList = self.getAllBtnList()

        if not state:
            self.delBtn.grid_forget()
            self.upBtn.grid_forget()
            index = 2
            for btn in vAllList:
                if btn in vbtnList:
                    btn.grid(row=0, column=index)
                else :
                    btn.grid_forget()
                index+=1
        else:
            self.delBtn.grid(row=0, column=0)
            for btn in vbtnList:
                btn.grid_forget()
            self.upBtn.grid(row=0, column=5)

    def createFrame(self, parent):
        lbFrame = tk.createLabelFrame(parent)
        lbFrame.grid(row=0,column=0,sticky='nsew')

        lbFrame.grid_rowconfigure(0,weight=1)
        lbFrame.grid_columnconfigure(1,weight=1)

        self.delBtn = tk.createBtn(lbFrame, '[ X ]', lambda: self.delItem())
        self.delBtn.grid(row=0, column=0)
        self.delBtn.config(fg='red')

        lbInfopar = tk.createFrame(lbFrame)

        lbInfopar.grid_rowconfigure(0,weight=1)
        lbInfopar.grid_columnconfigure(0,weight=1)

        self.lbInfo = tk.createLb(lbInfopar, self.getInfoName())
        self.lbInfo.grid(row=0,column=0,sticky='w')
        self.lbInfo.config(anchor='w')

        lbInfopar.grid(row=0,column=1,sticky='nsew')

        self.leftBtn = tk.createBtn(lbFrame, '<-', lambda: self.leftTime())
        self.leftBtn.grid(row=0, column=2)

        self.setBtn = tk.createBtn(lbFrame, ' + ', lambda: self.triggerTime())
        self.setBtn.grid(row=0, column=3)

        self.rightBtn = tk.createBtn(lbFrame, '->', lambda: self.rightTime())
        self.rightBtn.grid(row=0, column=4)

        self.upBtn = tk.createBtn(lbFrame, ' ^ ', lambda: self.moveItem())
        self.upBtn.grid(row=0, column=5)

        lbFrame.config(width=PFB_WIDTH)
        return lbFrame

    def getInfoName(self):
        return self.data["data"]
    def leftTime(self):
        return
    def rightTime(self):
        return
    def triggerTime(self):
        return

    def moveItem(self):
        self.qtType.moveItem(self)

    def delItem(self):
        self.qtType.delItem(self)
        self.frame.destroy()