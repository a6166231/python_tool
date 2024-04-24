import json
import os
import subprocess
import sys

absPath = ''
if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

CFG_JSON_PATH = os.path.join(absPath, 'cfg.json')
try:
    f = open(CFG_JSON_PATH, 'r', encoding='utf-8')
    cfgJson = json.loads(f.read())
    f.close()
    port = cfgJson["port"]
except Exception as e:
    port = 8080
subprocess.call(f"python -m http.server {port}", shell=True)
