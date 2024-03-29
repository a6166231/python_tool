

from tkinter import BaseWidget
from typing import Any
from prefabs.qtPrefabFact import createQTPrefabByType
from quickData import createTimeJumpPfbData, delTimeJumpPfbData, getTimeJumpPfbData, setTimeJumpPfbDatIndex
from tkGUI import tk

class QTTypeBtnBase:
    type:int
    width:int = 300
    height:int = 300
    def __init__(self , parent: BaseWidget, editState) -> None:
        self.parent = parent
        self.pfbData = getTimeJumpPfbData(self.type)
        self.vPrefabList = []
        self.editState = editState
        self.create()

    def create(self):
        self.frame = tk.createFrame(self.parent)
        self.customWidget = self.createCustomWidget(self.frame)
        self.customWidget.pack(fill='both', pady=3)

        self.customBtnList = self.createCustomBtnList(self.frame)

        self.frame.config(width=self.width, height=500)
        self.frame.pack_propagate(False)

    def delItem(self, qtBtn):
        self.vPrefabList.remove(qtBtn)
        delTimeJumpPfbData(self.type, qtBtn.data)
        self.sortAllPfbGrid()

    def moveItem(self, qtBtn):
        try:
            _index = self.vPrefabList.index(qtBtn)
            if _index != 0:
                self.vPrefabList.remove(qtBtn)
                self.vPrefabList.insert(_index-1, qtBtn)
                self.sortAllPfbGrid()
            setTimeJumpPfbDatIndex(self.type, qtBtn.data)
        except:
            pass

    def clear(self):
        for child in self.customBtnList.winfo_children():
            child.destroy()
        self.vPrefabList = []

    def sortAllPfbGrid(self):
        for i in range(len(self.vPrefabList)):
            btn = self.vPrefabList[i]
            btn.frame.grid(row = i)

    def createCustomWidget(self, parent):
        funBtnFrame = tk.createLabelFrame(parent)
        return funBtnFrame

    #自定义的时间点按钮列表
    def createCustomBtnList(self, parent):
        rect = tk.createLabelFrame(parent)
        rect.pack(fill='both', pady=3)

        view = tk.createViewRect(rect,width=self.width - 20, height=self.height)

        for pfb in self.pfbData:
            self.createCustomBtnItem(view, pfb)
        return view

    #自定义的时间点按钮列表
    def createCustomBtnItem(self, parent, pfb):
        _item = createQTPrefabByType(self , parent, pfb)
        _item.frame.grid(row=len(self.vPrefabList))

        self.vPrefabList.append(_item)
        return _item

    def setEditState(self, status:bool):
        self.editState = status
        for qt in self.vPrefabList:
            qt.setEditState(status)

    def getCustomBtnPrefabData(self)->Any:
        return

    # 生成自定义的按钮数据
    def createCustomBtnPrefabData(self):
        pfbData = self.getCustomBtnPrefabData()
        try:
            if pfbData and pfbData['data']:
                createTimeJumpPfbData(self.type, pfbData)
                self.createCustomBtnItem(self.customBtnList, pfbData)
                return
        except:
            pass
        print('create custom btn prefab data err~~', self)