#属性区域

from tkinter import BaseWidget
from ccc.cc import cc
from ccc.tree.track.nodeTrack import NodeTrack

class MainProperties:
    def __init__(self, frame_att:BaseWidget):
        self.frame_att = frame_att

    def onSelect(self, node:cc.Node):
        childrenKeys = list(self.frame_att.children.keys())
        for i in range(0, len(childrenKeys)):
            self.frame_att.children[childrenKeys[i]].destroy()
        if not node:
            print('node is not in tree!')
            return
        nodeTrack = NodeTrack()
        nodeTrack.create(self.frame_att, node)

