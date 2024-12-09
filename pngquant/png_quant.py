#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))

pngquantPath = os.path.join(absPath, 'pngquant.exe')

def quantPng(fpath):
    basename = os.path.basename(fpath)
    suffix = basename.split('.')[1]
    if suffix == 'png':
        print(' -', fpath)
        cmd = '%s --force %s --output=%s' % ( pngquantPath , fpath,fpath)
        os.system(cmd)

def traverse_folder_cfg(folder_path):
    if os.path.isfile(folder_path):
        quantPng(folder_path)
    else:
        print('+', folder_path)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                quantPng(os.path.join(root, file))

try:
    FPATH = './'
    try:
        FPATH = sys.argv[1]
    except:
        pass
    traverse_folder_cfg(FPATH)
    os.system('pause')
except Exception as e:
    print('报错拉', e)
    os.system('pause')