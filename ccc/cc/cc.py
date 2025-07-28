from msilib.schema import SelfReg
from re import split
from typing import Any, TypeVar
from enum import Enum

from numpy import number

from ccc.cc.ccutils.dwuuid import likeUUid,decodeUuid

"""
cocos creator 于py中的解析类
尽量让用法和cocos中用法相似，尽量保证属性、方法类型规范

example:
    pfbData = readPrefabDataByPath(pfbPath)
    pfb = Prefab()
    pfb.initPfbData(pfbData)
    vButtons = pfb.getRootNode().getComponentsInChildren(Button)
    node = pfb.getRootNode().getChildByName('test')
"""

NODE_ID = '__id__'
NODE_NAME = '_name'
NODE_CHILDREN = '_children'
NODE_COMPONENTS = '_components'
NODE_PREFAB = '_prefab'

PFB_TYPE = '__type__'
PFB_UUID = '__uuid__'
PFB_EXPECTED_TYPE = '__expectedType__'

# 基础对象结构
# 兼容 obj['key'] / obj.key / obj.get(key) / obj.get('key') 多种用法
#   - 即  button._transform, label._cacheMode ,  sprite._spriteFrame
class Object:
    id: int
    """ indexId in self prefab buffer array """
    def __init__(self):
        self.id = -1

    def __getattr__(self, key: str):
        return self.__getitem__(key)

    def get(self, key: str):
        return self.__getitem__(key)

    def __getitem__(self, key: str):
        try:
            return self.__getattribute__(key)
        except:
            return None

# 组件基类 目前基本上prefab中解析的所有的对象都继承于Component类
class Component(Object):
    node: 'Node'
    uuid: str
    name: str
    """ default data in prefab buffer array"""
    def __init__(self):
        super().__init__()
        self.node = None
        self.__data = None
        self.model = Object()
        self.uuid = ''
        self.name = __name__

    @staticmethod
    def TYPE(self):
        return self.__class__.__name__

    @property
    def data(self) -> dict:
        return self.__data

    def Type(self : 'Component'):
        return self.__class__.__name__

    @data.setter
    def data(self, data):
        self.model = formatData(data)
        self.__data = data

    def __getitem__(self, key: str):
        try:
            return self.__getattribute__(key)
        except:
            return self.model.__getitem__(key)

#目前只把需要的类型解析出来  再细的属性暂时还不需要 可以从父类的data里直接取
class Button(Component):
    #按钮的动画类型
    class TRANSITION(Enum):
        NONE = 0
        COLOR = 1
        SPRITE = 2
        SCALE = 3
    pass
class Sprite(Component):
    #Sprite 类型
    class SpriteType(Enum):
        # 普通类型。
        SIMPLE = 0,
        # 切片（九宫格）类型。
        SLICED = 1,
        # @zh  平铺类型
        TILED =  2,
        # 填充类型。
        FILLED = 3,
        # # 以 Mesh 三角形组成的类型
        # MESH: 4
    # 填充类型。
    class FillType(Enum):
        # 水平方向填充。
        HORIZONTAL = 0,
        # 垂直方向填充。
        VERTICAL = 1,
        # 径向填充
        RADIAL = 2,
    #精灵尺寸调整模式。
    class SizeMode(Enum):
        # 使用节点预设的尺寸。
        CUSTOM = 0,
        # 自动适配为精灵裁剪后的尺寸。
        TRIMMED = 1,
        # 自动适配为精灵原图尺寸。
        RAW = 2,

    spriteframe: str

    def __init__(self, spriteframe: str = ''):
        super().__init__()
        self.spriteframe = spriteframe
    

class Layout(Component):
    pass
class UITransform(Component):
    def __init__(self, width = 100, height = 100):
        super().__init__()
        self.width = width
        self.height = height

class BlockInputEvents(Component):
    pass

class Color(Component):
    def __init__(self, r=0, g=0, b=0, a=0, HEX=None,DEC=None):
        super().__init__()
        if HEX:
            self.formatHEX(HEX)
        elif DEC:
            self.formatDEC(DEC)
        else :
            self.r = r
            self.g = g
            self.b = b
            self.a = a

        self.DEC_RGB = '(%s,%s,%s)' % (self.r,self.g,self.b)
        self.DEC_RGBA = '(%s,%s,%s,%s)' % (self.r,self.g,self.b,self.a)

        self.HEX_REB = '#%s%s%s' % (hex(self.r)[2:],hex(self.g)[2:],hex(self.b)[2:])
        self.HEX_REBA = '#%s%s%s%s' % (hex(self.r)[2:],hex(self.g)[2:],hex(self.b)[2:],hex(self.a)[2:])

    def formatHEX(self, HEX:str):
        self.a = int(eval('0x'+HEX[7:])) if len(HEX) > 7 else 0
        self.b = int(eval('0x'+HEX[5:7]))
        self.g = int(eval('0x'+HEX[3:5]))
        self.r = int(eval('0x'+HEX[1:3]))

    def formatDEC(self, DEC:str):
        decData = split(DEC[2:len(DEC)-1],',')
        self.a = int(DEC[3])if len(decData) >= 4 else 0
        self.b = int(DEC[2])
        self.g = int(DEC[1])
        self.r = int(DEC[0])

class UIOpacity(Component):
    def __init__(self, opacity:int = 255):
        super().__init__()
        self.opacity = opacity
    pass
class Label(Component):
    #文本横向对齐类型
    class HorizontalTextAlignment(Enum):
        LEFT = 0,
        CENTER = 1,
        RIGHT = 2,
    #文本垂直对齐类型
    class VerticalTextAlignment(Enum):
        TOP = 0,
        CENTER = 1,
        BOTTOM = 2,
    #文本溢出行为类型
    class Overflow(Enum):
        NONE = 0,
        #CLAMP 模式中，当文本内容超出边界框时，多余的会被截断
        CLAMP = 1,
        #SHRINK 模式，字体大小会动态变化，以适应内容大小。这个模式在文本刷新的时候可能会占用较多 CPU 资源
        SHRINK = 2,
        #在 RESIZE_HEIGHT 模式下，只能更改文本的宽度，高度是自动改变的
        RESIZE_HEIGHT = 3,
    #文本图集缓存类型
    class CacheMode(Enum):
        NONE = 0,
        BITMAP = 1,
        CHAR = 2,
    def __init__(self):
        super().__init__()
        self.string = ''
        self.fontSize = 24
        self.lineHeight = 24

class LabelOutline(Component):
    pass
class RichText(Component):
    pass

class Vec2(Object):
    def __init__(self,x:int = 0,y:int = 0):
        super().__init__()
        self.x = x
        self.y = y
class Rect(Object):
    def __init__(self,x:int = 0,y:int = 0,widget:int = 100,height:int =100):
        super().__init__()
        self.x = x
        self.y = y
        self.width = widget
        self.height = height

T = TypeVar("T")
class Node(Component):
    name: str
    parent: 'Node'

    components: list['Component']
    children: list['Node']
    prefabInfo: 'PrefabInfo'

    position: 'Vec2'
    scale: 'Vec2'

    def __init__(self):
        super().__init__()
        self.name = "node"
        self.parent = None
        self.components = []
        self.children = []
        self.prefab = None
        self.position = Vec2()
        self.scale = Vec2()

    def init(self, data, id):
        self.id = id
        if data.get(NODE_NAME):
            self.name = data[NODE_NAME]
    def addComponent(self, com: 'Component'):
        com.node = self
        self.components.append(com)
    def setPrefabInfo(self, pfb: 'PrefabInfo'):
        pfb.node = self
        self.prefabInfo = pfb

    def addChild(self, child: 'Node'):
        child.parent = self
        self.children.append(child)
    def getChildren(self):
        return self.children

    def getChildByName(self, name: str) -> 'Node':
        for child in self.children:
            if child.name == name:
                return child
        return None

    def getComponentByType(self, t: type[T] | str) -> T:
        for com in self.components:
            if type(t) != str and issubclass(com.__class__, t):
                return com
            elif t == com.Type():
                return com
        return None
    # 从该节点的所有子节点中查找包含指定组件  
    # bSelf是否包含该节点
    def getComponentsInChildren(self, t: type[T] | str, bSelf: bool = True) -> list[T]:
        components = []
        if bSelf:
            for com in self.components:
                if type(t) != str and issubclass(com.__class__, t):
                    components.append(com)
                elif t == com.Type():
                    components.append(com)

        for child in self.children:
            components += child.getComponentsInChildren(t)
        return components

# prefab中关联的prefabinfo组件
# 对于prefab嵌套的情况目前只解析了uuid和fileid 还未把对应嵌套的预制体继续递归解析下去
# todo 递归解析嵌套的预制体
class PrefabInfo(Component):
    uuid: str
    fileId: str
    prefab: 'Prefab'

    def __init__(self):
        super().__init__()
        self.uuid = ''
        self.fileId = ''
        self.prefab = None

    def initPrefabInfo(self, buffer: dict):
        self.data = buffer
        self.__formatPrefabInfo()

    def __formatPrefabInfo(self):
        self.fileId = self.data['fileId']
        asset: dict = self.data['asset']
        if asset.get(PFB_EXPECTED_TYPE) and asset[PFB_EXPECTED_TYPE] == Prefab.TYPE(Prefab):
            self.uuid = asset[PFB_UUID]

#解析prefab预制体文件 同时作为prefab组件用
class Prefab(Component):
    root: 'Node'
    # info: 'PrefabInfo'
    # name: str

    def __init__(self):
        super().__init__()
        self.root = None
        # self.info = None
        # self.name = ''
        self._nodeObj = {}
        self._buffer = []

    def initPfbData(self, buffer: list[dict]):
        if len(buffer) == 0:
            print('pfb data length is 0!')
            return
        self._buffer = buffer
        # try:
        pfbData = self._buffer[0]["data"]
        rootNodeData = self._buffer[pfbData[NODE_ID]]
        self.root = self.getNodeById(pfbData[NODE_ID])
        self.__formatNode(rootNodeData, self.root)
        # except:
        #     print('init pfb data error!')
        #     pass

    def getRootNode(self) -> 'Node':
        return self.root
    # 根据id返回node对象
    def getNodeById(self, id) -> 'Node':
        if self._nodeObj.get(id):
            return self._nodeObj[id]
        else:
            data = self._buffer[id]
            node = Node()
            node.init(data, id)
            self._nodeObj[id] = node
            return node
    # 根据id返回component组件
    def getComponentById(self, id) -> [T]:
        com = getAutoComponentByType(self._buffer[id][PFB_TYPE])
        com.id = id
        com.data = self._buffer[id]
        return com
    # 根据id返回PrefabInfo
    def getPrefabInfoById(self, id) -> 'PrefabInfo':
        prefab = PrefabInfo()
        prefab.initPrefabInfo(self._buffer[id])
        return prefab
    #格式化节点
    def __formatNode(self, nodeData, node: 'Node'):
        #子节点列表整理
        if nodeData.get(NODE_CHILDREN):
            children = nodeData[NODE_CHILDREN]
            if len(children) > 0:
                for child in children:
                    cnode = self.getNodeById(child[NODE_ID])
                    self.__formatNode(self._buffer[child[NODE_ID]], cnode)
                    node.addChild(cnode)

        #节点组件列表整理
        if nodeData.get(NODE_COMPONENTS):
            components = nodeData[NODE_COMPONENTS]
            if len(components) > 0:
                for component in components:
                    com = self.getComponentById(component[NODE_ID])
                    node.addComponent(com)

        #prefab嵌套解析
        if nodeData.get(NODE_PREFAB):
            prefab = self.getPrefabInfoById(nodeData[NODE_PREFAB][NODE_ID])
            node.setPrefabInfo(prefab)

    # 当前prefab对象转字符串
    def dumps() -> str:
        return ''

#项目自定义脚本
class CustomScript(Component):
    uuid: str
    compressUUid: str

    def __init__(self):
        super().__init__()
        self.uuid = ''
        self.compressUUid = ''

    # 检测是不是一个项目自定义脚本
    @staticmethod
    def check(s: str) :
        #目前只要解析成功为uuid的都认为是一个自定义的脚本
        return likeUUid(s)

    @property
    def data(self) -> dict:
        return self.__data

    @data.setter
    def data(self, data):
        self.model = formatData(data)
        self.__data = data

        self.compressUUid = self.model[PFB_TYPE]
        self.uuid = decodeUuid(self.compressUUid)


T_OBJ = TypeVar('T_OBJ')
dictClass = {}

#指定类的指定子类
def getClsSubClassList(cls: T_OBJ) -> list[T_OBJ]:
    return cls.__subclasses__()

# 返回指定类的子类列表
def getClsSubList(cls: T_OBJ) -> list[T_OBJ]:
    if dictClass.get(type(cls)):
        return dictClass[type(cls)]
    else:
        d = getClsSubClassList(cls)
        dictClass[type(cls)] = d
        return d

#根据类型返回最合适的组件 找不到则用component
def getAutoComponentByType(t: str) -> Component:
    clsList = getClsSubList(Component)
    for cls in clsList:
        if COM_TYPE(cls, t):
            return cls()
    return Component()

#组件类型
def COM_TYPE(cls: Component, t: str) -> bool:
    #检测是可解析的组件还是自定义的脚本
    if cls == CustomScript:
        return CustomScript.check(t)
    else:
        return ('cc.' + cls.__name__) == t

def formatData(data: dict):
    obj = Object()
    for key in data:
        if type(data[key]) == dict:
            obj.__setattr__(key, formatData(data[key]))
        else:
            obj.__setattr__(key, data[key])
    return obj