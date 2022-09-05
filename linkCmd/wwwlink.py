import os,json,glob,shutil,time,socket
from win10toast import ToastNotifier
from colorama import Fore

BAT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(BAT_PATH)

start = time.clock()


conf = {}
if(os.path.exists('./conf.json')):
    f = open('./conf.json', 'r')
    conf = json.loads(f.read())
    f.close()

try:
    if conf["setLight"] >= 0:
        os.system("updateLight %s" % (conf["setLight"]))
except:
    pass


PROJECT_BINGO = conf["pName"][conf["buildIndex"]]

T_PPATH = conf["pAbsPath"] + PROJECT_BINGO + '/tools/texCompressor/'
T_CONFIG_JSON = T_PPATH + 'conf.json'

P_PPATH = conf["pAbsPath"] + PROJECT_BINGO + '/tools/package/'
P_CONFIG_JSON = P_PPATH + 'conf.json'

ASTC_PATH = conf["pAbsPath"] + PROJECT_BINGO + '/client/astc/'
OUTPUT_DIR_FASTEST = 'outputFastest'
OUTPUT_DIR_EXHAUSTIVE = 'outputExhaustive'

COMPRESS_EXE = 'compressor'
PACKAGE_EXE = 'package'

def pathExist(path):
    if not os.path.exists(path): 
        print("path is null: \"%s\"." % path)
        ToastNotifier().show_toast("ERROR","path is null: \"%s\"." % path,icon_path=None, duration=3,threaded=True)
        exit()

def delfile(path):
    # if(os.path.exists(path)):
    #     shutil.rmtree(path)
    fileNames = glob.glob(path + r'\*')
    for fileName in fileNames:
        try:
            os.remove(fileName)
        except:
            try:
                os.rmdir(fileName)
            except:
                delfile(fileName)
                os.rmdir(fileName)

def copyDir(src, dst,std=False,mt=20):
    # print(src,dst)
    stdStr = "" if std else ">nul"
    cmd = 'ROBOCOPY ' + src + ' ' + dst + " /E /MT:"+ str(mt) + " " + stdStr
    os.system(cmd)
    # shutil.copytree(src, dst)

def copyFile(start,end):
    shutil.copy(start, end)

if(conf["buildASTC"]):
    print("-1. start build astc~")
    pathExist(T_PPATH)

    os.chdir(T_PPATH)
    f = open(T_CONFIG_JSON)
    cfg = json.loads(f.read())
    f.close()
    cfg['cocosCreatorRoot'] = conf["cocosCreatorRoot"]
    cfg['useFastest'] = conf["useFastest"]
    cfg['updateBG'] = conf["updateBG"]
    f = open(T_CONFIG_JSON, 'w')
    f.write(json.dumps(cfg,indent=4))
    f.close()

    status = os.system('echo x|%s' % (COMPRESS_EXE))

    if status != 0:
        exit()

if conf["copyToClient"]:
    print("-2. start copy astc ")
    delfile(ASTC_PATH)
    outPath = OUTPUT_DIR_FASTEST if(conf["useFastest"]) else OUTPUT_DIR_EXHAUSTIVE
    copyDir(T_PPATH + outPath + '/' , ASTC_PATH)

if(conf["buildPackage"]):
    print("-3. start package")
    pathExist(P_PPATH)

    os.chdir(P_PPATH)
    f = open(P_CONFIG_JSON)
    cfg = json.loads(f.read())
    f.close()

    host_name=socket.gethostname()
    host=socket.gethostbyname(host_name)
    serverStr = "http://" + host +":3000/servers"
    for item in conf['entranceServerList']:
        if item != serverStr:
            print(Fore.YELLOW + "warning : " + item + " != " + serverStr + Fore.RESET)

    cfg['Windows']['gitPath'] = conf['gitPath']
    cfg['Windows']['cocosCreatorRoot'] = conf['cocosCreatorRoot']
    cfg['Windows']['bundleInMain'] = conf['bundleInMain']
    cfg['Windows']['entranceServerList'] = conf['entranceServerList']
    f = open(P_CONFIG_JSON, 'w')
    f.write(json.dumps(cfg,indent=4))
    f.close()
    status = os.system('echo x|%s' % (PACKAGE_EXE))
    if status != 0:
        exit()

if conf["copyToServer"]:
    print("-4. copy to server")
    VERSION_JSON_PATH = 'history/ver.json'
    pathExist(P_PPATH + VERSION_JSON_PATH)
    # rm all old version dirs
    delfile(conf["serverPath"] + "resource" )
    f = open(P_PPATH + VERSION_JSON_PATH, 'r')
    confV = json.loads(f.read())
    f.close()

    pathExist(P_PPATH + 'output/' + str(confV["versionCode"]))
    copyDir(P_PPATH + 'output/' + str(confV["versionCode"]), conf["serverPath"] + "resource/" + str(confV["versionCode"]))
    copyFile(P_PPATH + 'output/' + str(confV["versionCode"]) + '/version.json', conf["serverPath"])

end = time.clock()

print(Fore.GREEN +'------Success-----')
print('total cost time : ' + str(int(end - start)) + " s" +  Fore.RESET)
os.startfile(P_PPATH + 'package/simulator')
ToastNotifier().show_toast("Build Over", "Build Success", icon_path=None, duration=3,threaded=True)

if conf["install"]:
    print("install aab......")
    INSTALL_PATH = BAT_PATH + "\\..\\installAAB\\"
    os.chdir(INSTALL_PATH)
    INSTALL_EXE = "aab1"
    f = open('./conf.json', 'r')
    installCfg = json.loads(f.read())
    f.close()
    installCfg["buildIndex"] = conf["buildIndex"]
    f = open('./conf.json', 'w')
    f.write(json.dumps(installCfg, indent=4))
    f.close()
    status = os.system('echo x|%s' % (INSTALL_EXE))
    if status != 0:
        exit()
os.chdir(BAT_PATH)

f = open('./conf.json', 'r')
conf = json.loads(f.read())
f.close()


try:
    if conf["setLight"] >= 0:
        os.system("updateLight %s" % (100))
except:
    pass

endcmd = conf["endCalls"][str(conf["endCallIndex"])]
if(len(endcmd) != 0):
    os.system(endcmd)
os.system("pause")