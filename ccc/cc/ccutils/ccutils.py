#coding=utf-8


def formatBigFloat(val):
    if (len(str(val)) >= 23):
        return str(val)
    return float(val)
# 读取prefab数据
def readPrefabDataByPath(path: str):
    import json
    f = open(path,'r',encoding='utf-8')
    cfgJson = json.loads(f.read(),parse_float=formatBigFloat)
    f.close()
    return cfgJson

# 写入prefab数据
def writePrefabByData(path: str, cfgJson: list[any]):
    import json
    f = open(path,'w',encoding='utf-8')
    f.write(str(json.dumps(cfgJson,indent=2,ensure_ascii=False,default=formatBigFloat)))
    f.close()

#直接将字符串写入prefab  慎用
def customWritePrefabData(path: str, s: str):
    f = open(path,'w',encoding='utf-8')
    f.write(s)
    f.close()
