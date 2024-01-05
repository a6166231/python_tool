from tkinter import BaseWidget
from ccc.cc import cc
from ccc.tree.track.baseTrack import BaseTrack, TrackLineInfoType

MAP_COM = {
    cc.Sprite.__name__: ['color', 'spriteFrame'],
    cc.UITransform.__name__: ['width', 'height', 'anchorX', 'anchorY'],
    cc.Label.__name__: ['string', 'font', 'color', 'fontSize', 'lineHeight', 'cacheMode', ],
    cc.LabelOutline.__name__: ['color', 'width']
}

class ComponentTrack(BaseTrack):
    def create(self, parent:BaseWidget, component:cc.Component):
        self.component = component
        self.title = self.createTitle(parent, str(component.name), False, logCall=lambda:self.logCom(), checkCall=lambda:self.changeCom())
        self.componentPropertyList = []
        proList = MAP_COM.get(self.component.name) or []
        print(proList)
        for key in proList:
            lineInfo = self.createLineInfo(parent, key, str(self.component[key]), TrackLineInfoType[key], updateCall=lambda v:self.changeProperty(key, v))
            self.componentPropertyList.append(lineInfo)

    def changeProperty(self, key, v):
        print(key, v)
        pass

    def logCom(self):
        print(self.component)

    def changeCom(self):
        print('change com status')

    def cacheModeChange(self, val):
        print(val)
    def colorChange(self, val):
        print(val)