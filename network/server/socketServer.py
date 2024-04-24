
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),9090)) #绑定要监听的端口
s.listen(5)

while True:
    c,addr = s.accept()
    while True:
        data = c.recv(1024)  #接收数据
        print('服务器收到:',data.decode()) #打印接收到的数据
        c.send(data.upper()) #然后再发送数据
    c.close()