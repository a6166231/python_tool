
# 美术psd文件转cocos creator 中预制体文件
# ------------------------------------------------------------------
# 暂时弃了，记录下
# - py可以解析psd文件
# - cocos creator中每个版本的prefab文件部分字段不同
# - prefab中的一些字段有自己的一些生产规则 如：3.x的fileId字段，找不到生产算法
# - 组件、节点、prefabInfo结构（暂不确定是为了干什么）在json文件中的下标规则
#       理论上是无所谓顺序的，只要保证数据结构中的id字段对应的下标的对象是正确的即可
# - 用cocos creator的插件来实现是最符合prefab导出的，cc支持消息生产prefab文件没有以上的问题，但是使用流程上不认可
# ------------------------------------------------------------------

from psd_tools import PSDImage
from pypinyin import lazy_pinyin
import os,re

from ccc.cc.cc import Component, Label, Node, Sprite, UIOpacity, UITransform, Vec2
def mk_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


psd_file_name_map = {}
def format_str(s:str):
    #所有空格都替换为下划线
    s = re.sub(' +', '_', s)
    print('- ', s)
    #中文转为拼音
    s =  ''.join(lazy_pinyin(s))
    print('--- ', s)

    #防止文件重名
    if psd_file_name_map[s]:
        psd_file_name_map[s] = psd_file_name_map[s] + 1
    else:
        psd_file_name_map[s] = 0

    if psd_file_name_map[s] != 0:
        s = s + '_' + psd_file_name_map[s]

    return s
def psd_dump(path):
    global psd_file_name_map
    psd_file_name_map = {}
    (psd_dir, psd_name) = os.path.split(path)
    (psd_file, ext_name) = os.path.splitext(psd_name)

    img_out_dir = os.path.join(psd_dir, psd_file + '_img')
    mk_dir(img_out_dir)

    psd = PSDImage.open(path)

    root = group_layer(psd)
    print(root)

#psd的layer节点转cc的节点或组件
def psd_layer_to_node_or_component(layer) -> list[Component] | Component | None:
    #不显示的节点不要
    if not layer.is_visible():
        return None
    # print(layer.name, layer.kind, layer.offset)
    if layer.kind == 'type':
        return type_layer(layer)
    elif layer.kind == 'group':
        return group_layer(layer)
    elif layer.kind == 'pixel':
        return pixel_layer(layer)
    elif layer.kind == 'shape':
        return shape_layer(layer)
    else:
        return other_layer(layer)

#节点
def group_layer(parent):
    node = Node()
    node.name = parent.name

    for child in parent.descendants():
        comList = psd_layer_to_node_or_component(child)
        if not comList:
            continue

        childnode = Node()
        childnode.name = child.name

        if type(comList) == list:
            for i in range(len(comList)):
                node.addComponent(comList[i])
        elif type(comList) == Component:
            node.addComponent(comList)

        #设置节点的uitransform
        size = child.size
        node.addComponent(UITransform(size[0], size[1]))

        #设置节点坐标
        node.position = Vec2(child.left, child.top)

        #非透明组件增加uiopacity
        if child.opacity != 255:
            childnode.addComponent(UIOpacity(child.opacity))

        node.addChild(childnode)
    return node

#具有字体或段落的文本和样式信息的图层。
def type_layer(layer):
    fontSize = int(24)
    try:
        rundata = layer.engine_dict['StyleRun']['RunArray'][0]
        fontSize = int(rundata['StyleSheet']['StyleSheetData']['FontSize'])
    except:
        print('text font size error: ', layer.name)
        pass
    lb = Label()
    lb.string = layer.text
    lb.fontSize = fontSize
    return lb

#图片层
def pixel_layer(layer):
    if not layer.has_pixels():
        return None
    img = layer.topil()
    if not img:
        return None
    spf = Sprite()
    return spf

#在矢量蒙版中绘制的图层
def shape_layer(layer):
    return

def other_layer(layer):
    return

psd_dump('./test.psd')