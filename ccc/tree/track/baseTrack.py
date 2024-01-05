from enum import Enum
from tkinter import LEFT, RIGHT, BaseWidget
from typing import Any, Callable
from ccc.cc import cc

from tkGUI.tk import createBtn, createCheckBtn, createColorChoose, createDropList, createEdit, createFrame, createLb,createRect
#标题块
class TrackTitle:
    def __init__(self, parent: BaseWidget, name:str ,btnLogShow: bool = False, logCall:Callable|str = '', drawCall:Callable|str = '', checkCall:Callable|str = '') -> None:
        self.widget = createFrame(parent)
        self.widget.pack(fill='x')

        self.checkBox = createCheckBtn(self.widget, name, command=checkCall)
        self.checkBox.pack(side=LEFT)

        # self.lbName = createLb(self.widget,name)
        # self.lbName.pack(side=LEFT)
        if btnLogShow:
            self.btnLog = createBtn(self.widget, 'log', command=logCall)
            self.btnLog.pack(side=RIGHT)

        self.btnDraw = createBtn(self.widget, 'draw', command=drawCall)
        self.btnDraw.pack(side=RIGHT)

class TrackLineInfoType(Enum):
    string = 1,
    number = 2,
    color = 3,
    cacheMode = 4,
    font = 5,
    spriteFrame = 6,

#行信息块
class TrackLineInfo:
    def __init__(self, parent: BaseWidget, key:str,val:Any, type:TrackLineInfoType,updateCall:Callable) -> None:
        self.widget = createFrame(parent)
        self.widget.pack(fill='x')

        self.lbName = createLb(self.widget,key)
        self.lbName.pack(side=LEFT,padx=50)

        if type == TrackLineInfoType.number or type == TrackLineInfoType.string:
            self.createEditLb(self.widget, val, updateCall)
        elif type == TrackLineInfoType.cacheMode:
            self.createCharMode(self.widget, val , updateCall)
        elif type == TrackLineInfoType.spriteFrame or type == TrackLineInfoType.font:
            self.createEditLb(self.widget, val , updateCall)
            self.lbVal.config(state='readonly')
        elif type == TrackLineInfoType.color:
            self.createColorChoose(self.widget, val=val, updateCall=updateCall)

    def createEditLb(self, parent: BaseWidget, val: str, updateCall:Callable):
        self.lbVal = createEdit(parent, val, updateCall)
        self.lbVal.pack(side=RIGHT,padx=30)

    # 文本char模式的展示
    def createCharMode(self, parent: BaseWidget, val: str = '0', updateCall:Callable | None = None):
        cacheModeList = list(cc.Label.CacheMode)
        vCacheModel = []
        vCacheModelVal = []
        for char in cacheModeList:
            vCacheModel.append(char.name)
            vCacheModelVal.append(char.value[0])
        index = vCacheModelVal.index(int(val)) or 0
        self.char = createDropList(parent, vCacheModel ,vCacheModel[index], selectCall=updateCall)
        self.char.pack(side=RIGHT,padx=30)

    #颜色选择器
    def createColorChoose(self, parent: BaseWidget, val: tuple | None = None, updateCall:Callable | None = None):
        colorVal = '#FFFFFF'
        if type(val) == tuple:
            colorVal = val[1]
        elif val != None:
            colorVal = str(val)
        try:
            if self.colorChoose and val != None and self.color.DEC_RGBA == cc.Color(HEX=colorVal).DEC_RGBA:
                return self.color.DEC_RGBA
            self.colorChoose.destroy()
        except:
            pass
        
        self.color = cc.Color(HEX=colorVal)
        self.colorChoose = createRect(parent, cc.Rect(0,0,100,20), colorVal, '#000000')
        self.colorChoose.pack(side=RIGHT,padx=30)
        #点击打开拾色器 并在选择颜色之后 清除掉当前颜色
        if updateCall:
            self.colorChoose.bind('<Button-1>', lambda e: updateCall(self.createColorChoose(parent, createColorChoose(parent),updateCall)))
        else:
            self.colorChoose.bind('<Button-1>', lambda e: self.createColorChoose(parent, createColorChoose(parent), updateCall))
        return colorVal

class BaseTrack:
    def createTitle(self, parent:BaseWidget, name:str, btnLogShow: bool, logCall:Callable|str = '', drawCall:Callable|str = '', checkCall:Callable|str = '')->TrackTitle:
        return TrackTitle(parent, name, btnLogShow,logCall,drawCall,checkCall)

    def createLineInfo(self, parent: BaseWidget, key:str, val:str, type: TrackLineInfoType, updateCall:Callable=None)->TrackLineInfo: # type: ignore
        return TrackLineInfo(parent, key, val, type, updateCall)
