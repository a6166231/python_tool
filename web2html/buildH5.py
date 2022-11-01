#!/usr/bin/python3
import json

f = open('./conf.json', 'r')
cfg = json.loads(f.read())
PPATH = cfg['ppath']
HTML_PATH = cfg['htmlPath']

