from os import chdir
from typing import Any, TypeVar
from ccc.cc import cc
T_OBJ = TypeVar('T_OBJ')

#指定类的指定子类
def getClsSubClassList(cls: T_OBJ) -> list[T_OBJ]:
    return cls.__subclasses__()

#根据类型返回最合适的组件 找不到则用component
def getAutoComponentByType(t: str) -> cc.Component:
    clsList = cc.getClsSubList(cc.Component)
    for cls in clsList:
        if COM_TYPE(cls) == t:
            return cls()
    return cc.Component()

#组件类型
def COM_TYPE(cls: cc.Component) -> str:
    return 'cc.' + (cls.__name__ or '')

def formatData(data: dict):
    obj = cc.Object()
    for key in data:
        if type(data[key]) == dict:
            obj.__setattr__(key, formatData(data[key]))
        else:
            obj.__setattr__(key, data[key])
    return obj


def formatBigFloat(val):
    if (len(str(val)) >= 23):
        return str(val)
    return float(val)

def readPrefabByPath(path: str):
    import json
    f = open(path,'r',encoding='utf-8')
    cfgJson = json.loads(f.read(),parse_float=formatBigFloat)
    f.close()
    return cfgJson

def dumpPrefabByData(path: str, cfgJson: list[Any]):
    import json
    f = open(path,'w',encoding='utf-8')
    f.write(str(json.dumps(cfgJson,indent=2,ensure_ascii=False,default=formatBigFloat)))
    f.close()

def dumpNodeToObj(node:cc.Node, indentation: int = 0):
    lvNow = indentation * '  '
    lvNext = (indentation + 1) * '  '
    s = lvNow + '{\n'
    s += '%s%s: %s,\n' % (lvNext, 'name', node.name)
    s += '%s%s: %s,\n' % (lvNext, 'uuid', node.uuid)
    s += '%schildren:[' % (lvNext)
    for child in node.children:
        s += '\n%s' % dumpNodeToObj(child, indentation + 2)
    s += '%s],\n' % (lvNext if len(node.children) > 0 else '')
    s += lvNow + '},\n'
    return s