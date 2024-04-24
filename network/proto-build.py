
import os,sys
import subprocess
absPath=''
if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(absPath, 'proto'))

try:
    subprocess.run('protoc -I=. *.proto --python_out="../proto_out"', shell=True)
except Exception as e:
    print(e)

print(' - end - ')
os.system('pause')