
from tkinter import BaseWidget
from ccc.cc import cc
from ccc.cc.ccutils.ccutils import dumpNodeToObj
from ccc.tree.track.baseTrack import TrackLineInfoType
from ccc.tree.track.componentTrack import ComponentTrack

class NodeTrack(ComponentTrack):
    def create(self, parent:BaseWidget, node:cc.Node | None):
        print(node)
        if not node:
            return
        self.node = node
        title = self.createTitle(parent, 'Node' , True , logCall=lambda:self.logNode(), drawCall=lambda:self.drawNode(), checkCall=lambda:self.checkVisible())
        self.title = title
        self.name = self.createLineInfo(parent,'name', node.name,  TrackLineInfoType.string, updateCall=lambda *e:self.nameChange(e))
        self.x = self.createLineInfo(parent,'x', str(node.position.x), TrackLineInfoType.number, updateCall=lambda *e:self.xChange(e))
        self.y = self.createLineInfo(parent,'y', str(node.position.y),  TrackLineInfoType.number, updateCall=lambda *e:self.yChange(e))
        self.scaleX = self.createLineInfo(parent,'scaleX', str(node.scale.x),  TrackLineInfoType.number, updateCall=lambda *e:self.scaleXChange(e))
        self.scaleY = self.createLineInfo(parent,'scaleY', str(node.scale.y),  TrackLineInfoType.number, updateCall=lambda *e:self.scaleYChange(e))

    def logNode(self):
        print(dumpNodeToObj(self.node))

    def drawNode(self):
        print('draw')

    def checkVisible(self):
        print('change active')

    def nameChange(self, e):
        print(self.name.lbVal.get())
    def xChange(self, e):
        print(self.x.lbVal.get())
    def yChange(self, e):
        print(self.y.lbVal.get())
    def scaleXChange(self, e):
        print(self.scaleX.lbVal.get())
    def scaleYChange(self, e):
        print(self.scaleY.lbVal.get())