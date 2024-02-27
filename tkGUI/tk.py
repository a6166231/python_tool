from tkinter import HORIZONTAL, VERTICAL, BaseWidget, Checkbutton, LabelFrame, OptionMenu, Scrollbar, StringVar, Tk,Canvas, Radiobutton,Label,Button,Entry,Frame,colorchooser
from tkinter.font import Font
from tkinter.ttk import Treeview
from typing import Callable

from ccc.cc import cc

def createWindow(name:str, width: int = 100, height: int = 100, x: int = 0, y: int = 0):
    win = Tk()
    win.title(name)

    geoStr = '%sx%s' % (width, height)
    if x > 0:
        geoStr+='+%s' % x
    elif x < 0:
        geoStr+=str(x)
    if y > 0:
        geoStr+='+%s' % y
    elif y < 0:
        geoStr+=str(y)
    win.geometry(geoStr)
    win['bg'] = 'gray'
    win.attributes("-alpha", 0.95)
    return win

def createFrame(parent:BaseWidget|Tk):
    w = Frame(parent)
    return w

def createViewRect(main:BaseWidget | Tk, width:int, height:int):
    canvas = createCanvas(main,width,height)
    canvas.pack(side='left', fill='both', expand=True)
    frame = createMask(canvas, width,height)
    frame.pack(fill='both')
    return frame

def createScrollBar(parent:BaseWidget, bHor:bool = False):
    bar=Scrollbar(parent,orient=HORIZONTAL if bHor else VERTICAL)
    return bar

def createMask(canvas: Canvas, width:int = 100, height: int = 100):
    rollFrame=createFrame(canvas)     # 在画布上创建frame
    canvas.create_window((0,0),window=rollFrame,anchor='nw')
    def myfunction(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    rollFrame.bind("<Configure>",myfunction)
    return rollFrame

def createCanvas(parent:BaseWidget | Tk, width:int = 100, height: int = 100):
    canvas = Canvas(parent, width=width,height=height)
    return canvas

def createLb(parent: BaseWidget, string: str = '', size=12):
    lb = Label(parent, text=string,font=Font(size=size))
    return lb

def createLabelFrame(parent: BaseWidget, string: str = '', size=12):
    lb = LabelFrame(parent, text=string, font=Font(size=size))
    return lb

def createCheckBtn(parent:BaseWidget, string: str= '', command:Callable|str = ''):
    checkBtn = Checkbutton(parent, text=string, command = command)
    checkBtn.toggle()
    return checkBtn

def createBtn(parent: BaseWidget, string: str = '', command:Callable|str = ''):
    btn = Button(parent, name=string, text=string, command=command)
    return btn
def createRadioBtn(parent: BaseWidget, radio_var, string: str = '', command:Callable|str = ''):
    btn = Radiobutton(parent, text=string,value=string, variable=radio_var,command=command, )
    return btn

def createEdit(parent: BaseWidget, string: str, updateCall:Callable | None = None):
    edit = Entry(parent,textvariable=StringVar())
    edit.insert(0,string)
    if updateCall:#更新监听
        edit.bind("<KeyRelease>", lambda e: updateCall())
    return edit

def createRect(parent: BaseWidget, rect: cc.Rect = cc.Rect(), color: str='white', outline:str ='black'):
    canvas = createCanvas(parent, width=rect.width, height=rect.height)
    canvas.pack()
    if color == None:
        color = 'white'
    x1, y1 = rect.x,rect.y
    x2, y2 = x1 + rect.width , y1 + rect.height
    canvas.create_rectangle(x1,y1,x2,y2,fill=str(color),outline=outline)
    return canvas

def createColorChoose(parent: BaseWidget):
    return colorchooser.askcolor(parent=parent)

def createDropList(parent: BaseWidget, string: list[str], default: str, selectCall:Callable | None=None):
    vars = StringVar()
    vars.set(default)
    if selectCall:
        vars.trace('w',lambda a,b,c: selectCall(vars.get()))
    drop = OptionMenu(parent,vars,*string)
    return drop

def createStringVar(string:str):
    return StringVar(value=string)

def createTree(parent: BaseWidget, height:int=300):
    tree = Treeview(parent,displaycolumns=(),height=height)
    return tree

def createCCNodeTree(parent: BaseWidget, data:list[cc.Node], height:int=300):
    tree = createTree(parent,height)
    def insertTreeNode(tree: Treeview, node:cc.Node, parent:str = ''):
        leaf = tree.insert(parent, 'end', text=node.name,iid=node.uuid)
        for child in node.children:
            insertTreeNode(tree, child, leaf)

    for node in data:
        insertTreeNode(tree, node)
    return tree

def createFont():
    font=('italic', 16)
    return font