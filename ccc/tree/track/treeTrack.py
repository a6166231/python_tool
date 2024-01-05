
from tkinter import BaseWidget
from typing import Callable
from ccc.cc import cc
from ccc.tree.track.baseTrack import BaseTrack
from tkGUI import tk

class TreeTrack(BaseTrack):
    def create(self, parent: BaseWidget, data:list[cc.Node]):
        tree = tk.createCCNodeTree(parent, data,200)
        tree.bind('<<TreeviewSelect>>', func= lambda e: self.leafSelect())
        tree.pack(expand=False, fill='both')
        self.tree = tree
        self.data = {}
        def deepForeach(node:cc.Node):
            if self.data.get(node.uuid):
                print('node uuid is repeat', node)
            self.data[node.uuid] = node
            for child in node.children:
                deepForeach(child)
        for item in data:
            deepForeach(item)

    def leafSelect(self):
        if self.commond:
            selectItems = self.getSelect()
            if len(selectItems) == 0:
                return
            print(selectItems[0])

            node = self.getNodeDataByIId(selectItems[0])
            self.commond(self,node)

    def getSelect(self):
        return self.tree.selection()

    def selectCommond(self, commond:Callable):
        self.commond = commond

    def getNodeDataByIId(self, iid: str):
        return self.data[iid]