from .models import *
import pymysql
import socket
import time
import datetime
from django.http import *
from django.forms import *
from threading import *
import traceback

# 服务器启动状态
state = 0


def get_state():
    global state
    return state


def server(host, port, rate):
    global server_receive, state
    state = 1
    try:
        server_receive = socket.socket()
        server_receive.bind((host, port))
        server_receive.listen(5)
        print(server_receive.gettimeout())
        print(server_receive.getsockname())
        print("listening")
        conns, addr = server_receive.accept()
        while True:
            conns.settimeout(10)
            # server_receive.setblocking(flag=0)
            # print(conns.gettimeout())
            # print(conns.getpeername())
            if state == 0:
                break
            update_pro = list(DataProject.objects.filter(update_flag=1).values_list('name', 'id', 'begin_time'))
            length = len(update_pro)
            if len(update_pro) == 0:
                continue
            # print(server_receive.getpeername())
            db = pymysql.connect('127.0.0.1', 'root', '123456', 'db2')
            cursor = db.cursor()  # 创建游标
            try:
                for i in update_pro:
                    timesstamp = time.mktime(datetime.datetime.now().timetuple())
                    rela_time = int(timesstamp - time.mktime(i[2].timetuple()))
                    # print(i[0].split('_')[1])
                    msg = '$gh' + i[0].split('_')[1] + '#'
                    # msg = "$gh50LA#"  # 发送消息
                    # print(msg)
                    conns.sendall(bytes(msg, encoding="utf-8"))  # 接受消息

                    data = conns.recv(10000)
                    data = str(data, encoding="utf-8")
                    # print(data)
                    list1 = data.split(';')
                    # list1.pop(0)
                    list1[0] = list1[0].split(i[0].split('_')[1])[1]
                    list1[-1] = list1[-1][0:-2]
                    field = 'PROJECT_ID,RELATIVETIME'
                    field_data = str(i[1]) + ',' + str(rela_time)
                    for j in list1:
                        field += (',' + j.split(':')[0])
                        field_data += (',' + j.split(':')[1])
                    sql = 'insert into data_online(' + field + ') values (' + field_data + ')'
                    # print(sql)
                    cursor.execute(sql)  # 执行SQL语句
                    db.commit()
                cursor.close()
                print(db)
                db.close()
                time.sleep(rate)
            except:
                # print()
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                traceback.print_exc()
                # raise
                # print(time.localtime())
                print("conns close")
                conns.close()
                conns, addr = server_receive.accept()

                continue

    except OSError:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        raise


# global connections
# connections = server_receive.accept()
# print(type(connections))
# print("connecting")
# conn()
threads = []


def connect(request):
    host = request.POST.get('address')
    port = int(request.POST.get('ip'))
    thetype = request.POST.get('type')
    rate = int(request.POST.get('rate'))
    global state, threads, t1, server_receive  # 定义状态信号，线程列表，线程，服务器
    state = 0
    message = "服务器重新启用"
    if len(threads) != 0:
        server_receive.close()
    if thetype == '打开':
        if len(threads) == 0:
            message = "服务器开启"
        t1 = Thread(target=server, args=(host, port, rate))
        threads = [t1]
        try:
            t1.start()
        except OSError:
            raise
    else:
        threads = []
        message = "服务器已关闭"
        # server(host, port, rate)
        # threads[0].close()
    print(message)
    print(threads)
    return JsonResponse({"message": message})
