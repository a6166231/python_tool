#!/usr/bin/python3
import json
import os
from html.parser import HTMLParser
import base64
import simplejson
import math
import tinify
import os.path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

settingMatchKey = '{#settings}'
mainMatchKey = '{#main}'
engineMatchKey = '{#cocosengine}'
projectMatchKey = '{#project}'
resMapMatchKey = '{#resMap}'
spinePreviewMatchKey = '{#spinePreview}'
ttfMapMatchKey = '{#ttfMap}'

fileByteList = ['.png', '.jpg', '.mp3', '.ttf', '.plist', 'txt']

base64PrefixList = {
  '.png' : 'data:image/png;base64,',
  '.jpg' : 'data:image/jpeg;base64,',
  '.mp3' : '',
  '.ttf' : '',
  '.plist' : 'data:text/plist;base64,'
}

def read_in_chunks(filePath):
    extName = os.path.splitext(filePath)[1]
    if extName in fileByteList:
        file_object = open(filePath, 'rb')
        base64Str = base64.b64encode(file_object.read())
        base64Prefix = base64PrefixList[extName]
        if base64Prefix != None:
            base64Str = bytes(base64Prefix) + base64Str
            return base64Str
    elif extName == '':
        return None

    file_object = open(filePath)
    return file_object.read()

def writeToPath(path, data):
    with open(path,'w') as f:
        f.write(data)

def getResMap(jsonObj, path, resPath):
    fileList = os.listdir(path)
    for fileName in fileList:
        absPath = path + '/' + fileName
        if (os.path.isdir(absPath)):
            getResMap(jsonObj, absPath, resPath)
        elif (os.path.isfile(absPath) and absPath.find("main/index.js") == -1):
            dataStr = read_in_chunks(absPath)
            if dataStr != None:
                absPath = absPath.replace(resPath + '/', '')
                jsonObj[absPath] = dataStr

def getResMapScript(resPath):
    jsonObj = {}
    getResMap(jsonObj, resPath, resPath)
    jsonStr = simplejson.dumps(jsonObj)
    resStr = str("window.resMap = ") + jsonStr
    return resStr

# This issue is fixed in Cocos Creator 2.x
def fixEngineError(engineStr):
    newEngineStr = engineStr.replace("t.content instanceof Image", "t.content.tagName === \"IMG\"", 1)
    return newEngineStr

def addPlistSupport(mainStr):
    newMainStr = mainStr.replace("json: jsonBufferHandler,", "json: jsonBufferHandler, plist: jsonBufferHandler,", 1)
    return newMainStr

def integrate(projectRootPath, newHtmlPath):
    htmlPath = projectRootPath + '/build/web-mobile/index.html'
    settingScrPath = projectRootPath + '/build/web-mobile/src/settings.js'
    mainScrPath = projectRootPath + '/build/web-mobile/main.js'
    engineScrPath = projectRootPath + '/build/web-mobile/cocos2d-js.js'
    projectScrPath = projectRootPath + '/build/web-mobile/assets/main/index.js'
    resPath = projectRootPath + '/build/web-mobile/assets'
    indexInternalScrPath = projectRootPath + '/build/web-mobile/assets/internal/index.js'

    htmlStr = read_in_chunks(htmlPath)
    settingsStr = read_in_chunks(settingScrPath)
    htmlStr = htmlStr.replace(settingMatchKey, settingsStr, 1)

    projectStr = read_in_chunks(projectScrPath)
    htmlStr = htmlStr.replace(projectMatchKey, projectStr, 1)

    mainStr = read_in_chunks(mainScrPath)
    mainStr = addPlistSupport(mainStr)
    htmlStr = htmlStr.replace(mainMatchKey, mainStr, 1)

    engineStr = read_in_chunks(engineScrPath)
    engineStr = fixEngineError(engineStr)
    htmlStr = htmlStr.replace(engineMatchKey, engineStr, 1)

    resStr = getResMapScript(resPath)
    htmlStr = htmlStr.replace(resMapMatchKey, resStr, 1)

    writeToPath(newHtmlPath, htmlStr)

    targetFileSize = os.path.getsize(newHtmlPath)
    targetFileSizeInMegabyte = math.ceil(targetFileSize * 1000 / (1024 * 1024)) / 1000

    print("===================  All Done! =================== ")
    print("Target file = {}, with size {}M".format(newHtmlPath, targetFileSizeInMegabyte))


fileType = [".png", ".jpg"]
  
def isSupportedFile(filename):
    name, ext = os.path.splitext(filename)
    if ext in fileType:
        return True
    return False

def tinifyPic(targetPath):
    for filename in os.listdir(targetPath):
        filepath = os.path.join(targetPath, filename)
        if os.path.isdir(filepath):  
            tinifyPic(filepath) 
        else:  
            if isSupportedFile(filepath):
                print("Compressing: ", filepath)
                compressed_file = tinify.from_file(filepath)
                compressed_file.to_file(filepath)


f = open('./conf.json', 'r')
cfg = json.loads(f.read())
PPATH = cfg['ppath']
htmlPath = cfg['htmlPath']
projectRootPath = PPATH
resPath = projectRootPath + '/build/web-mobile/assets'
integrate(projectRootPath, htmlPath + '/index.html')
os.system('pause')