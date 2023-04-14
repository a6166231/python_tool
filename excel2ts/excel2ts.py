#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import os,json

BAT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(BAT_PATH)

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

TYPE_DICT = {
    'int': NUMBER,
    'byte': NUMBER,
    'float': NUMBER,
    'short': NUMBER,
    'double': NUMBER,
    'long': NUMBER,
    
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

def getTypeByStr(s, p = []):
    try:
        val = TYPE_DICT[s]
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
d = {}

def formatExcel(file_name:str):
    fp = os.path.join(FPATH, file_name)
    ts_text = "/**\n"

    EXCEL_NAME = file_name.split(".")[0]
    CLS_NAME = formatClsName(EXCEL_NAME)

    try:
        data = pd.read_csv(fp,header=None)
    except:
        try:
            data = pd.read_excel(fp,header=None)
        except:
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

    with open("%s/%s.ts" % (OPATH ,CLS_NAME), "w", encoding='utf-8') as f:
        f.write(ts_text)
    print('output %s.ts ' % CLS_NAME)

for file_name in os.listdir(FPATH):
    formatExcel(file_name)

print('\n - over - ')
os.system('pause')