import sys,os,json

if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

os.chdir(absPath)

CFG_JSON_PATH = './cfg.json'

cfgJson = {"data":{}}

def SetJsonData():
    f = open(CFG_JSON_PATH,'w',encoding='utf-8')
    f.write(str(json.dumps(cfgJson,indent=4,ensure_ascii=False)))
    f.close()

def quickTimeInit():
    if os.path.exists(CFG_JSON_PATH):
        global cfgJson
        f = open(os.path.join(CFG_JSON_PATH),'r',encoding='utf-8')
        cfgJson = json.loads(f.read())
        f.close()
    else :
        SetJsonData()

def createTimeJumpPfbData(index, data):
    pfbData = getTimeJumpPfbData(index)
    pfbData.append(data)
    SetJsonData()

def delTimeJumpPfbData(index, data):
    try:
        pfbData = getTimeJumpPfbData(index)
        pfbData.remove(data)
        SetJsonData()
    except Exception as e:
        print(e)

def setTimeJumpPfbDatIndex(index, data):
    try:
        pfbData = getTimeJumpPfbData(index)
        _index = pfbData.index(data)
        if _index != 0:
            pfbData.remove(data)
            pfbData.insert(_index-1, data)
            SetJsonData()
    except Exception as e:
        print(e)


def clearAll():
    cfgJson["data"] = {}
    SetJsonData()

def getTimeJumpPfbData(index):
    key = str(index)
    typeData = cfgJson["data"].get(key)
    if not typeData:
        typeData = {}
        cfgJson["data"][key] = typeData

    pfbData = typeData.get('pfbData')
    if not pfbData:
        pfbData = []
        typeData['pfbData'] = pfbData
        SetJsonData()
    return pfbData

