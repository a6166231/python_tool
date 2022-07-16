import os,sys,shutil
wutilPath = os.path.dirname(os.path.abspath(__file__))
os.chdir(wutilPath)
f = open(wutilPath + '/myapplication.pth', 'w')
f.write(wutilPath)
f.close()
pypath = os.path.join(os.path.dirname(sys.executable),"lib","site-packages")
pthpython = pypath + '/myapplication.pth'
if os.path.exists(pthpython ):
    exit()
shutil.copyfile(wutilPath + '/myapplication.pth', pthpython)