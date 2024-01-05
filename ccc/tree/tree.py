#节点树区域
from tkinter import BaseWidget
from typing import Any, Callable
from ccc.tree.track import treeTrack
from ccc.cc import cc

testData = []
for i in range(0,30):
    test_node = cc.Node()
    test_node.name = str(i)
    test_node.uuid = test_node.name
    test_node.addComponent(cc.Sprite())

    for j in range(0, 20):
        test_node2 = cc.Node()
        test_node2.name = "%s_%s" % (i,j)
        test_node2.uuid = test_node2.name
        test_node2.addComponent(cc.Label())
        test_node.addChild(test_node2)
    testData.append(test_node)

class MainTree:
    def __init__(self, frame_tree:BaseWidget, data:list[Any] = testData):
        self.frame_tree = frame_tree
        self.tree = treeTrack.TreeTrack()
        self.tree.create(frame_tree, data)

    def selectCommond(self, command:Callable):
        self.tree.selectCommond(command)

    def getSelect(self):
        return self.tree.getSelect()