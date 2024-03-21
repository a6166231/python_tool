#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import os, json, sys

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
        except:
            try:
                if len(code) == 0:
                    data = pd.read_excel(fp, header=None)
                else:
                    data = pd.read_excel(fp, header=None, encoding=code)
                result = 2
                break
            except:
                pass
    if result < 0:
        print('cant open excel file!  ', FPATH)
    return result, data


def formatExcel(file_name: str):
    fp = os.path.join(FPATH, file_name)
    EXCEL_NAME = os.path.basename(file_name.split(".")[0])
    CLS_NAME = formatClsName(EXCEL_NAME)
    result, data = TryOpenExl(fp)
    if result < 0:
        return

    columns = data.columns.tolist()
    #头部注释
    #excel名
    ts_text = "/**\n * \n * excel : %s\n" % (EXCEL_NAME)
    #excel导出对应的configmanager中的名字
    ts_text += " public %s: { [key: number]: %s } = {};\n" % (
        EXCEL_NAME.replace('cfg_', ''), CLS_NAME)
    ts_text += " */\n"

    #export interface部分
    ts_text += 'export interface %s {\n' % CLS_NAME
    for i in columns:
        ts_text += '\t/** %s */\n' % data.at[DESC_INDEX, i]
        ptype = getTypeByStr(data.at[TYPE_INDEX, i])
        if ptype == ANY:
            try:
                ptype = getValueType(data.at[DATA_INDEX, i])
            except:
                pass
        ts_text += '\t%s: %s;\n' % (data.at[PARAM_INDEX, i], ptype)
    ts_text += '}\n'

    if not os.path.exists(OPATH):
        os.makedirs(OPATH)

    global bAddLongImport
    if bAddLongImport:
        ts_text = LONGPATH + ts_text
        bAddLongImport = False

    with open("%s/%s%s" % (OPATH, CLS_NAME, SUFFIX_NAME),
              "w",
              encoding='utf-8') as f:
        f.write(ts_text)
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

if FPATH.find('tables.xls') > 0:
    dirName = os.path.dirname(FPATH)
    result, data = TryOpenExl(FPATH)
    if result > 0:
        count = data.describe()[0]['count']
        for i in range(1, count):
            cfg = data.at[i, 0]
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
# import subprocess

# INFO_PATH = '%s/_info.txt' % OPATH
# ERROR_PATH = '%s/_error.txt' % OPATH

# def checkTsLint():
#     print('- start ts check - ')

#     f = open(INFO_PATH,'w')
#     f.write('')
#     f.close()
#     f = open(ERROR_PATH,'w')
#     f.write('')
#     f.close()

#     # try:
#     if not os.path.exists('%s/tsconfig.json' % (OPATH)):
#         os.chdir(OPATH)
#         cmd = 'tsc --init'
#         p = subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#         p.wait()
#         p.kill()

#         # os.system(cmd)
#     cmd = 'tsc -p %s --outDir %s/tsc' % (OPATH,OPATH)
#     f = open(INFO_PATH)
#     p = subprocess.Popen(cmd,shell=False,stdout=f,stderr=subprocess.STDOUT)
#     p.wait()
#     p.kill()
#     # except:
#     #     print('hava no tsc, check fail! ')
#     print('- check over - ')

# try:
#     if cfgJson["bCheckError"]:
#         checkTsLint()
# except:
#     pass
# print('\n - failList :  %s - ' % failList)
print('\n - total out put ts:  %s - ' % tsCount)
os.system('pause')
