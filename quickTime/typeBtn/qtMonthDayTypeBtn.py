from tkinter import BaseWidget, Button
from tkGUI import tk

class QTMonthDayTypeBtn:
    @staticmethod
    def create(parent:BaseWidget):
        frame = tk.createFrame(parent)

        customWidget = QTMonthDayTypeBtn.createCustomWidget(frame)
        customWidget.grid(row=0,column=0)

        customBtnList = QTMonthDayTypeBtn.createCustomBtnList(frame)
        customBtnList.grid(row=1,column=0,pady=5)

        return frame

    #自定义的时间点导出按钮
    @staticmethod
    def createCustomWidget(parent):
        funBtnFrame = tk.createLabelFrame(parent)
        funBtnFrame.config(width=300,height=50)

        return funBtnFrame

    #自定义的时间点按钮列表
    @staticmethod
    def createCustomBtnList(parent):
        funBtnFrame = tk.createLabelFrame(parent)
        funBtnFrame.config(width=300,height=300)

        return funBtnFrame

