import json,os,sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))

f = open('./conf.json')
conf = json.loads(f.read())
f.close()

def updateConf(path,val):
    f = open(path + '/conf.json')
    tempConf = json.loads(f.read())
    f.close()
    tempConf['isListener'] = val

    f = open(path + '/conf.json', 'w')
    f.write(json.dumps(tempConf,indent=4))
    f.close()

updateConf('../../wweather', conf['weather'])
