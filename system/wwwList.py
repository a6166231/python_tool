# -*- coding: utf-8 -*-
import json,os,sys
f = open('./cmdList.json', 'r')
CMD_INFO_LIST = json.loads(f.read())
CMD_LIST = []
reload(sys) 
sys.setdefaultencoding('utf8')
f.close()
i_index = 0

for s in CMD_INFO_LIST:
    i_index+=1
    s_cmd = str(i_index) + '. '
    s_cmd += s['cmd']
    s_cmd += '(' + s['desc'] + ')'
    CMD_LIST.append(s['cmd'])
    print(s_cmd)

try:
    select_index = int(input('select cmd:'))
    if (not select_index) or (select_index == 0):
        os.system('exit')
    cmdObj = CMD_INFO_LIST[select_index - 1]
    if cmdObj:
        vParmas = []
        try:
            for parmas in cmdObj['parmas']:
                s = parmas
                p = input(s)
                vParmas.append(str(p))
        except:
            pass
        # print(cmdObj['cmd'] + ' ' + ' '.join(vParmas))
        os.system(cmdObj['cmd'] + ' ' + ' '.join(vParmas))
except:
    pass