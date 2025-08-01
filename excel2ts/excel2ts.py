#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, sys
import pandas as pd

if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

os.chdir(absPath)

f = open(os.path.join('./cfg.json'), 'r', encoding='utf-8')
cfgJson = json.loads(f.read())
f.close()

FPATH = cfgJson['excel_path']
try:
    if sys.argv[1]:
        FPATH = sys.argv[1]
except:
    pass

OPATH = cfgJson['out_path']

if len(OPATH) == 0:
    OPATH = './out/'

DESC_INDEX = cfgJson['desc_line']
TYPE_INDEX = cfgJson['type_line']
PARAM_INDEX = cfgJson['param_line']
DATA_INDEX = cfgJson['data_line']

SUFFIX_NAME = cfgJson['suffix']
MERGE_STATUS = cfgJson['merge']

ANY = 'any'
NUMBER = 'number'
ARRAY = 'Array<%>'
STRNIG = 'string'
LONG = 'Long'

LONGPATH = 'import { Long } from "core";\n\n'

TYPE_DICT = {
    'int': NUMBER,
    'byte': NUMBER,
    'float': NUMBER,
    'short': NUMBER,
    'double': NUMBER,
    'long': LONG,
    'Long': LONG,
    'uint': NUMBER,
    'ushort': NUMBER,
    'ubyte': NUMBER,
    'string': STRNIG,
}

TYPE_PY = {
    int: NUMBER,
    float: NUMBER,
    str: STRNIG,
}

bAddLongImport = False
bAddLongImported = False

def getTypeByStr(s, p=[]):
    try:
        val = TYPE_DICT[s]
        if val == LONG:
            print('       - import Long')
            global bAddLongImport
            bAddLongImport = True
        return val
    except:
        return ANY


def getValueType(val):
    try:
        val = int(val)
        return TYPE_PY[type(val)]
    except:
        try:
            val = str(val)
            return TYPE_PY[type(val)]
        except:
            return ANY


def formatClsName(className):
    className = className.replace('cfg', '').replace('config', '')
    names = className.split('_')
    for index in range(len(names)):
        if len(names[index]) > 0:
            names[index] = names[index][0].upper() + names[index][1:]
    return "".join(names) + 'Config'


# data = {}
# 试图通过不同的编码格式打开excal
def TryOpenExl(fp):
    encodes = ['', 'gbk', 'utf-8']
    result = -1
    data = {}
    for code in encodes:
        try:
            if len(code) == 0:
                data = pd.read_csv(fp, header=None)
            else:
                data = pd.read_csv(fp, header=None, encoding=code)
            result = 1
            break
        except Exception as e:
            # print('error1 :', e)
            try:
                if len(code) == 0:
                    data = pd.read_excel(fp, header=None)
                else:
                    data = pd.read_excel(fp, header=None, encoding=code)
                result = 2
                break
            except Exception as e2:
                # print('error2 :', e2)
                pass
    if result < 0:
        print('cant open excel file!  ', FPATH)
    return result, data


ts_text = ""

def deepFormatKeysStr(keys: list, t: str):
    if len(keys) == 0:
        return t
    ss = "{ [%s: number]: %s }" % (keys[0], deepFormatKeysStr(keys[1:], t))
    return ss

def formatExcel(file_name: str):
    fp = os.path.join(FPATH, file_name)
    EXCEL_NAME = os.path.basename(file_name.split(".")[0])
    CLS_NAME = formatClsName(EXCEL_NAME)
    result, data = TryOpenExl(fp)
    if result < 0:
        return

    columns = data.columns.tolist()
    #头部注释
    global ts_text

    #excel名
    ts_text += "/**\n * excel : %s\n" % (EXCEL_NAME)
    #excel导出对应的configmanager中的名字
        
    ts_text += " public %s: " % (EXCEL_NAME.replace('cfg_', ''))

    if EXCEL_NAME in tableKeyMap:
        ts_text += deepFormatKeysStr(tableKeyMap[EXCEL_NAME], CLS_NAME)
    else:
        ts_text += deepFormatKeysStr(['key'], CLS_NAME)
    ts_text += " = {};"
    ts_text += "\n */\n"

    #export interface部分
    ts_text += 'export interface %s {\n' % CLS_NAME
    for i in columns:
        if pd.isna(data.at[PARAM_INDEX, i]):
            continue
        ts_text += '\t/** %s */\n' % data.at[DESC_INDEX, i]
        ptype = getTypeByStr(data.at[TYPE_INDEX, i])
        key = str(data.at[PARAM_INDEX, i]).strip().rstrip()

        if ptype == ANY:
            try:
                ptype = getValueType(data.at[DATA_INDEX, i])
            except:
                pass

        ts_text += '\t%s: %s;\n' % (key, ptype)
    ts_text += '}\n'

    if not os.path.exists(OPATH):
        os.makedirs(OPATH)

    global bAddLongImport
    global bAddLongImported

    if bAddLongImport:
        bAddLongImported = True
        if not MERGE_STATUS:
            ts_text = LONGPATH + ts_text
        bAddLongImport = False

    if not MERGE_STATUS:
        with open("%s/%s%s" % (OPATH, CLS_NAME, SUFFIX_NAME),
                  "w",
                  encoding='utf-8') as f:
            f.write(ts_text)
        ts_text = ""
    else:
        ts_text += '\n'
    global tsCount
    tsCount += 1
    print('output %s%s ' % (CLS_NAME, SUFFIX_NAME))


tsCount = 0


def forEachPath():
    if os.path.isdir(FPATH):
        for file_name in os.listdir(FPATH):
            formatExcel(file_name)
    elif os.path.isfile(FPATH):
        formatExcel(FPATH)
    else:
        failList.append(FPATH)
        print('cfg[excel_path] is error: -- ' + FPATH)


excalEndName = ['.xls', '.csv']
failList = []

tableCfgData = {}
tableKeyMap = {}

TABLE_PATH = FPATH

if FPATH.find('tables.xls') > 0:
    pass
else:
    TABLE_PATH = os.path.join(os.path.dirname( FPATH), 'tables.csv')

try:
    result, data = TryOpenExl(TABLE_PATH)
    if result > 0:
        tableCfgData = data
        count = data.describe()[0]['count']
        for i in range(1, count):
            if pd.isna(data.at[i, 2]):
                continue
            lkey = str.split(data.at[i, 2], '#')
            l = []
            for item in lkey:
                l.append(item)
            tableKeyMap[data.at[i, 0]] = l
except Exception as e:
    print(e)
    pass

if FPATH.find('tables.xls') > 0:
    if result > 0:
        dirName = os.path.dirname(FPATH)
        count = tableCfgData.describe()[0]['count']
        for i in range(1, count):
            cfg = tableCfgData.at[i, 0]
            fp = os.path.join(dirName, cfg)
            bExists = False
            for end in excalEndName:
                if os.path.exists(fp + end):
                    bExists = True
                    formatExcel(fp + end)
                    break
            if not bExists:
                failList.append(fp)
else:
    forEachPath()

if MERGE_STATUS:

    if bAddLongImported:
        ts_text = LONGPATH + ts_text

    with open("%s/%s%s" % (OPATH, "ConfigType", SUFFIX_NAME),
              "w",
              encoding='utf-8') as f:
        f.write(ts_text)
    pass

print('\n - total out put ts:  %s - ' % tsCount)
os.system('pause')
