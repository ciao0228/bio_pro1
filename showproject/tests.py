from django.test import TestCase

# Create your tests here.
import socket
from threading import Timer
import time

server_receive = socket.socket()
# 确定IP
ip_port = ("127.0.0.1", 61234)
# bind()绑定
server_receive.bind(ip_port)
# listen监听
server_receive.listen(5)
# 建立客户端链接
# accept 接受请求链接

qh = '50la'
count = 0

global timer


def connect():
    msg = '$gh50LA#'
    conn.sendall(bytes(msg, encoding="utf-8"))
    # 接受消息
    print("sending")
    data = conn.recv(10000)
    print("getting")
    print(str(data, encoding="utf-8"))
    global count
    count = count + 5
    print(count)
    global timer
    if count >= 11:
        timer.cancel()
    else:
        timer = Timer(5, connect)
        timer.start()


while True:
    # 接受数据
    print("listening")
    conn, addr = server_receive.accept()
    print("connecting")
    connect()
    # msg = "50la"
    # conn.sendall(bytes(msg, encoding="utf-8"))
    # # 接受消息
    # data = conn.recv(10000)
    # print(str(data, encoding="utf-8"))
