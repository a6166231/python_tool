
import os,zipfile
BUNDLE = '7'
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PPATH = os.getcwd()

def compress(path, zipFilePath):
    dirName = os.path.dirname(zipFilePath)
    if(not os.path.exists(dirName)):
        os.makedirs(dirName)
    zipf = zipfile.ZipFile(zipFilePath, 'w')
    if os.path.isfile(path):
        pre_len = len(os.path.dirname(path))
        arcname = path[pre_len:].strip(os.path.sep)
        zipf.write(path, arcname)
    else:
        pre_len = len(os.path.dirname(path))
        for parent, dirnames, filenames in os.walk(path):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)
                zipf.write(pathfile, arcname)
    zipf.close()

compress('./' + BUNDLE, './0.zip')
os.system('rd /s /q ' + BUNDLE + ' >nul')