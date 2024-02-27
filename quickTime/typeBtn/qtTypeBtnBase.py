

from tkinter import BaseWidget
from typing import Any, Callable
from prefabs.qtPrefabFact import createQTPrefabByType

from tkGUI import tk

QT_TYPE_TRACK_WIDTH = 300
QT_TYPE_TRACK_HEIGHT = 300

class QTTypeBtnBase:
    def __init__(self , parent: BaseWidget, createCall:Callable, pfbData) -> None:
        self.createCall = createCall
        self.parent = parent
        self.pfbData = pfbData
        self.create()

    def create(self):
        self.frame = tk.createFrame(self.parent)
        self.customWidget = self.createCustomWidget(self.frame)
        self.customWidget.pack(fill='both', pady=3)

        self.customBtnList = self.createCustomBtnList(self.frame)
        self.customBtnList.pack(fill='both', pady=3)

        self.frame.config(width=QT_TYPE_TRACK_WIDTH, height=500)
        self.frame.pack_propagate(False)

    def clear(self):
        for child in self.customBtnList.winfo_children():
            child.destroy()

    def createCustomWidget(self, parent):
        funBtnFrame = tk.createLabelFrame(parent)
        return funBtnFrame

    #自定义的时间点按钮列表
    def createCustomBtnList(self, parent):
        rect = tk.createLabelFrame(parent)
        rect.config(width=QT_TYPE_TRACK_WIDTH, height=QT_TYPE_TRACK_WIDTH)
        # rect.pack_propagate(False)
        # funBtnFrame = tk.createViewRect(rect, QT_TYPE_TRACK_WIDTH, QT_TYPE_TRACK_HEIGHT)
        # funBtnFrame.pack()
        for pfb in self.pfbData:
            btn = self.createCustomBtnItem(rect, pfb)
            btn.frame.config(width=QT_TYPE_TRACK_WIDTH-10)
        return rect

    #自定义的时间点按钮列表
    def createCustomBtnItem(self, parent, pfb):
        _item = createQTPrefabByType(pfb['type'] , parent, pfb)
        return _item

    def getCustomBtnPrefabData(self)->Any:
        return

    # 生成自定义的按钮数据
    def createCustomBtnPrefabData(self):
        pfbData = self.getCustomBtnPrefabData()
        print(pfbData)
        try:
            if pfbData and pfbData['type'] and pfbData['data']:
                self.createCall(pfbData)
                self.createCustomBtnItem(self.customBtnList, pfbData)
                return
        except:
            pass
        print('create custom btn prefab data err~~', self)