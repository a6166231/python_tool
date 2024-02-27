

from tkinter import Widget
from typing import Callable
from prefabs.qtPrefabFact import createQTPrefabByType

from tkGUI import tk

QT_TYPE_TRACK_WIDTH = 300
QT_TYPE_TRACK_HEIGHT = 300

class QTTypeBtnBase:
    def __init__(self, frame: Widget, createCall:Callable, pfbData) -> None:
        self.createCall = createCall
        self.frame = frame
        self.pfbData = pfbData
        # childrenKeys = list(frame.children.keys())
        # self.pfbFactFrame = frame.children[childrenKeys[0]]
        # self.pfbListFrame = frame.children[childrenKeys[1]]

    #自定义的时间点按钮列表
    @staticmethod
    def createCustomBtnList(parent, qt: 'QTTypeBtnBase'):
        funBtnFrame = tk.createLabelFrame(parent)
        for pfb in qt.pfbData:
            _item = createQTPrefabByType(pfb['type'] ,funBtnFrame, pfb)
            _item.frame.config(width=QT_TYPE_TRACK_WIDTH)

        return funBtnFrame