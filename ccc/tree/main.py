
import subprocess

#主入口
def createMainView():
    from tkinter import BaseWidget, Tk
    from ccc.tree.properties import MainProperties
    from ccc.tree.tree import MainTree
    from tkGUI import tk

    def createViewRect(main:BaseWidget | Tk, width:int, height:int):
        frame = tk.createViewRect(main, width,height)
        return frame

    # 主窗口
    main = tk.createWindow(name='tree',width=500,height=600)
    # 节点树层级区域
    frame_tree = createViewRect(main, 300, 300)
    # 节点属性区域
    frame_att = createViewRect(main, 300, 300)

    tree = MainTree(frame_tree)
    properties = MainProperties(frame_att)

    tree.selectCommond(lambda tree, node: properties.onSelect(node))#点击回调
    # 进入消息循环
    main.mainloop()

# import os
# def get_process_pid(processname:str):
#     # 定义一个空列表，放置按空格切割split(' ')后的进程信息
#     process_info_list = []
#     # 命令行输入，获取进程信息
#     process = os.popen('ps -A | grep %s'% processname)
#     # 读取进程信息，获取字符串
#     process_info = process.read()
#     print(process_info)
#     # 按空格切割split(" ")，
#     for i in process_info.split(' '):
#         # 判断不为空，添加到process_info_list中
#         if i != "":
#             process_info_list.append(i)
#     print(process_info_list)
#     # 列表第0位是字符串类型pid，转换成int类型，方便执行stop_process()
#     pid = int(process_info_list[0])
#     # 返回值是int类型pid
#     return pid

# print(get_process_pid('原始传奇'))

p = subprocess.Popen('E:/projects/python_tool/ccc/tree/main.exe', shell=True)

import lupa,sys,subprocess
from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)
print(sys.argv)
A = sys.argv[1]
a = lua.eval('%s' % A)


# createMainView()