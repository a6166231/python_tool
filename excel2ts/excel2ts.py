#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import os,json,sys

if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

os.chdir(absPath)


f = open(os.path.join('./cfg.json'),'r',encoding='utf-8')
cfgJson = json.loads(f.read())
f.close()

FPATH = cfgJson['excel_path']
OPATH = cfgJson['out_path']

DESC_INDEX = cfgJson['desc_line']
TYPE_INDEX = cfgJson['type_line']
PARAM_INDEX = cfgJson['param_line']
DATA_INDEX = cfgJson['data_line']

ANY = 'any'
NUMBER = 'number'
ARRAY = 'Array<%>'
STRNIG = 'string'
LONG = 'Long'

LONGPATH = 'import { Long } from "../net/Long";\n\n'

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

def getTypeByStr(s, p = []):
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
    className = className.replace('cfg','').replace('config','')
    names = className.split('_')
    for index in range(len(names)):
        if len(names[index]) > 0:
            names[index] = names[index][0].upper()+ names[index][1:]
    return "".join(names) +'Config'

data = {}

# 试图通过不同的编码格式打开excal
def TryOpenExl(fp):
    global data
    encodes = ['','gbk','utf-8']
    result = -1
    for code in encodes:
        try:
            if len(code) == 0:
                data = pd.read_csv(fp,header=None)
            else :
                data = pd.read_csv(fp,header=None,encoding=code)
            result = 1
            break
        except:
            try:
                if len(code) == 0:
                    data = pd.read_excel(fp,header=None)
                else :
                    data = pd.read_excel(fp,header=None,encoding=code)
                result = 2
                break
            except:
                pass
    return result

def formatExcel(file_name:str):
    fp = os.path.join(FPATH, file_name)
    ts_text = "/**\n"

    EXCEL_NAME = file_name.split(".")[0]
    CLS_NAME = formatClsName(EXCEL_NAME)

    result = TryOpenExl(fp)
    if result < 0:
        print('cant open excel file!  ',fp)
        return

    columns = data.columns.tolist()
    ts_text += " * \n"
    ts_text += " * excel : %s\n" % (EXCEL_NAME)
    ts_text+=' */\n'

    ts_text+= 'export interface %s {\n' % CLS_NAME
    for i in columns:
        ts_text += '\t/** %s */\n' % data.at[DESC_INDEX, i]
        ptype = getTypeByStr(data.at[TYPE_INDEX, i])
        if ptype == ANY:
            ptype = getValueType(data.at[DATA_INDEX, i])
        ts_text += '\t%s: %s;\n' % (data.at[PARAM_INDEX, i], ptype)
    ts_text+= '}\n'

    if not os.path.exists(OPATH):
        os.makedirs(OPATH)

    if  bAddLongImport:
        ts_text = LONGPATH + ts_text

    with open("%s/%s.ts" % (OPATH ,CLS_NAME), "w", encoding='utf-8') as f:
        f.write(ts_text)
    print('output %s.ts ' % CLS_NAME)

for file_name in os.listdir(FPATH):
    formatExcel(file_name)

print('\n - over - ')
os.system('pause')