from typing import TypeVar
from cc import *

T_OBJ = TypeVar('T_OBJ')

#指定类的指定子类
def getClsSubClassList(cls: T_OBJ) -> list[T_OBJ]:
    return cls.__subclasses__()

#根据类型返回最合适的组件 找不到则用component
def getAutoComponentByType(t: str) -> Component:
    clsList = getClsSubList(Component)
    for cls in clsList:
        if COM_TYPE(cls) == t:
            return cls()
    return Component()

#组件类型
def COM_TYPE(cls: Component) -> str:
    return 'cc.' + cls.__name__

def formatData(data: dict):
    obj = Object()
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

def dumpPrefabByData(path: str, cfgJson: list[any]):
    import json
    f = open(path,'w',encoding='utf-8')
    f.write(str(json.dumps(cfgJson,indent=2,ensure_ascii=False,default=formatBigFloat)))
    f.close()