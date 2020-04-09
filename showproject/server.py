import socket
import random

server_receive = socket.socket()
# 确定IP
ip_port = ("localhost", 10010)
# bind()绑定
server_receive.bind(ip_port)
# listen监听
server_receive.listen(5)
# 建立客户端链接
# accept 接受请求链接

qh = '50la'

while True:
    # 接受数据
    conn, addr = server_receive.accept()
    data = conn.recv(1024)
    # if not data:
    #     break
    # else:
    print(str(data, encoding="utf-8"))
    msg = str(data, encoding="utf-8") + ';TEMP:' + str(round((random.uniform(10, 20)), 10)) + ";F:" + str(
        round((random.uniform(10, 20)), 10)) + ";ADO:" + str(round((random.uniform(10, 20)), 10)) + ";PH1:" + str(
        round((random.uniform(10, 20)), 10)) + ";V:" + str(round((random.uniform(10, 20)), 10)) + ";EO2:" + str(
        round((random.uniform(10, 20)), 10)) + ";ECO2:" + str(round((random.uniform(10, 20)), 10)) + ";RPM:" + str(
        round((random.uniform(10, 20)), 10)) + ";OD1:" + str(round((random.uniform(10, 20)), 10)) + ";AF1:" + str(
        round((random.uniform(10, 20)), 10)) + ";AF2:" + str(round((random.uniform(10, 20)), 10)) + ";AF3:" + str(
        round((random.uniform(10, 20)), 10)) + ";RF1:" + str(round((random.uniform(10, 20)), 10)) + ";RF2:" + str(
        round((random.uniform(10, 20)), 10)) + ";RF3:" + str(round((random.uniform(10, 20)), 10)) + ";P:" + str(
        round((random.uniform(10, 20)), 10)) + ";AF4:" + str(round((random.uniform(10, 20)), 10)) + ";AF5:" + str(
        round((random.uniform(10, 20)), 10)) + ";AF6:" + str(round((random.uniform(10, 20)), 10)) + ";RF4:" + str(
        round((random.uniform(10, 20)), 10)) + ";RF5:" + str(round((random.uniform(10, 20)), 10)) + ";RF6:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR1:" + str(round((random.uniform(10, 20)), 10)) + ";ONR2:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR3:" + str(round((random.uniform(10, 20)), 10)) + ";ONR4:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR5:" + str(round((random.uniform(10, 20)), 10)) + ";ONR6:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR7:" + str(round((random.uniform(10, 20)), 10)) + ";ONR8:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR9:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR10:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR11:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR12:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR13:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR14:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR15:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR16:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR17:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR18:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR19:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONR20:" + str(round((random.uniform(10, 20)), 10)) + ";OUR:" + str(
        round((random.uniform(10, 20)), 10)) + ";CER:" + str(round((random.uniform(10, 20)), 10)) + ";RQ:" + str(
        round((random.uniform(10, 20)), 10)) + ";KLA:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONCALC1:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONCALC2:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONCALC3:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONCALC4:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONCALC5:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONCALC6:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONCALC7:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONCALC8:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONCALC9:" + str(
        round((random.uniform(10, 20)), 10)) + ";ONCALC10:" + str(round((random.uniform(10, 20)), 10)) + "#"
    conn.sendall(bytes(msg, encoding="utf-8"))
    # 关闭连接
    conn.close()
# server_receive.close()
