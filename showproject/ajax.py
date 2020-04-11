# 此文件用于处理页面发送的请求

from .data import *
from django.http import *
import pymysql
import time
import datetime
from django.utils import timezone
from django.db import connection

pro_name_id = dict(list(DataProject.objects.values_list('name', 'id')))


# import requests
def field_data(request):
    field = request.POST.get('field')
    the_type = request.POST.get('the_type')
    pro_id = request.POST.get('pro_id')
    last = request.POST.get("last")
    db = pymysql.connect('127.0.0.1', 'root', '123456', 'db2')  # 连接数据库
    cursor = db.cursor()  # 创建游标
    # 第一次访问数据
    if len(last) == 0:
        if the_type == 'on':
            sql1 = "select *,unix_timestamp(SAMPLE_TIME)  from data_online where PROJECT_id=" + str(pro_id)
        else:
            sql1 = "select *,unix_timestamp(SAMPLE_TIME)  from data_offline where PROJECT_id=" + str(pro_id)
    else:
        if the_type == "on":
            sql1 = "select " + field + ",unix_timestamp(SAMPLE_TIME)  from data_online where PROJECT_id=" + str(
                pro_id) + " and unix_timestamp(sample_time) > " + str(last)
        else:
            sql1 = "select " + field + ",unix_timestamp(SAMPLE_TIME)  from data_offline where PROJECT_id=" + str(
                pro_id) + " and unix_timestamp(sample_time) > " + str(last)
        # SQL语句
    # print(sql1)
    cursor.execute(sql1)  # 执行SQL语句
    data = cursor.fetchall()  # 查询到所有的数据存储到all_users中
    cursor.close()
    db.close()
    response = JsonResponse(data, safe=False)
    return response


# 历史参数获取
def his_field(request):
    name = request.POST.get('field')  # 获得选取的字段信息
    the_type = request.POST.get('the_type')  # 获取字段类型
    pro_name = request.POST.get("pro_name")
    pro_id = DataProject.objects.filter(name=pro_name).values_list("id", flat=True)[0]
    print(request.POST)
    if the_type == "on":
        data = list(DataOnline.objects.filter(project_id=pro_id).values_list('relativetime', name))
        min1 = list(Onrangemin.objects.filter(project_id=pro_id).values_list(name, flat=1))
        max1 = list(Onrangemax.objects.filter(project_id=pro_id).values_list(name, flat=1))
    else:
        data = list(DataOffline.objects.filter(project_id=pro_id).values_list("relativetime", name))
        min1 = list(Offrangemin.objects.filter(project_id=pro_id).values_list(name, flat=1))
        max1 = list(Offrangemax.objects.filter(project_id=pro_id).values_list(name, flat=1))
    response = JsonResponse({'data': data, 'min': min1[0], 'max': max1[0]})
    return response


# 历史分批数据获取
def his_pro(request):
    # pro_name_id = dict(list(DataProject.objects.values_list('name', 'id')))
    print(request.POST)
    pro_id = request.POST.get('pro_id')
    field = request.POST.getlist("field")
    the_type = request.POST.get('the_type')
    print(field)
    # 获取数据
    if the_type == 'on':
        data = DataOnline.objects.filter(project_id=pro_id).values_list(*field, 'relativetime')
        min1 = Onrangemin.objects.filter(project_id=pro_id).values(*field)
        max1 = Onrangemax.objects.filter(project_id=pro_id).values(*field)
        response = JsonResponse({'min': list(min1), 'max': list(max1), "data": list(data)})
        print(data)
    else:
        data = DataOffline.objects.filter(project_id=pro_id).values_list(*field, 'relativetime')
        min1 = Offrangemin.objects.filter(project_id=pro_id).values(*field)
        max1 = Offrangemax.objects.filter(project_id=pro_id).values(*field)
        response = JsonResponse({'min': list(min1), 'max': list(max1), "data": list(data)})
        print(data)
    return response


# ajax历史分批数据交互


def show_off(request):
    response = JsonResponse({"sss": 'pro_data'})
    return response


# 测试用


#
#
#
#
#
#
#
#
#
#
# 实时分批数据

# 创建项目
def create(request):
    new_pro = request.POST.get('host')  # 获取get()请求
    upload = request.POST.get('upload')  # 通过get()请求获取前段提交的数据
    db = pymysql.connect('127.0.0.1', 'root', '123456', 'db2')  # 连接数据库
    cursor = db.cursor()  # 创建游标
    sql1 = "select name from data_project where name=" + repr(new_pro)  # SQL语句

    cursor.execute(sql1)  # 执行SQL语句
    all_users = cursor.fetchall()  # 查询到所有的数据存储到all_users中

    if len(all_users) == 0:
        # 创建项目
        sql2 = "insert into data_project(NAME,update_flag,TEXT,BEGIN_TIME) values(%s,%s,%s,%s)"
        cursor.execute(sql2, (new_pro, 1, new_pro, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        # 获取项目id
        sql = "select id from data_project where name=" + repr(new_pro)
        cursor.execute(sql)
        pro_id = cursor.fetchall()[0][0]
        # 创建在线项目取值范围
        setrange(cursor, pro_id)
        response = JsonResponse({"data": 0})
    else:
        response = JsonResponse({"data": 1})
    db.commit()
    cursor.close()
    db.close()
    return response


# 保存离线数据记录
def save_values(request):
    data = dict(request.POST)
    print(data)
    for i in data:
        data[i] = data[i][0]
    data["PROJECT_id"] = int(data["PROJECT_id"])
    data["RELATIVETIME"] = int(data["RELATIVETIME"])
    data["UPLOAD"] = int(data["UPLOAD"])
    default = {"PROJECT_id": data["PROJECT_id"], "UPLOAD": data["UPLOAD"], "RELATIVETIME": data["RELATIVETIME"]}
    # print(default)
    DataOffline.objects.update_or_create(defaults=default, **data)
    db = pymysql.connect('127.0.0.1', 'root', '123456', 'db2')  # 连接数据库
    cursor = db.cursor()  # 创建游标
    # 获取所有离线数据
    sql1 = "select *,unix_timestamp(SAMPLE_TIME)  from data_offline where RELATIVETIME=" + str(data["RELATIVETIME"])
    cursor.execute(sql1)  # 执行SQL语句
    data = cursor.fetchall()[-1]  # 查询到所有的数据存储到data中
    cursor.close()
    db.close()
    # print(data)
    response = JsonResponse({"data": data})
    return response


# 打开,关闭项目更新
def open_close(request):
    the_type = request.POST.get('type')
    chosen_name = request.POST.getlist('chosen_name[]')
    db = pymysql.connect('127.0.0.1', 'root', '123456', 'db2')
    # 创建游标
    cursor = db.cursor()
    # SQL语句
    if the_type == 'open':
        for i in chosen_name:
            sql = 'update data_project set UPDATE_FLAG = 1 where NAME ="' + i + '"'
            cursor.execute(sql)
    else:
        for i in chosen_name:
            sql = 'update data_project set UPDATE_FLAG = null  where NAME ="' + i + '"'
            cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    global pro_name_id
    pro_name_id = dict(list(DataProject.objects.values_list('name', 'id')))
    response = JsonResponse({"data": 0})
    return response


# 离线事件记录
def event_values(request):
    data = dict(request.POST)
    for i in data:
        data[i] = data[i][0]
    db = pymysql.connect('127.0.0.1', 'root', '123456', 'db2')
    cursor = db.cursor()  # 创建游标
    sql = 'select count(TIME) from data_event where PROJECT_ID="' + data["project_id"] + '" and TIME="' + data[
        "time"] + '"'
    cursor.execute(sql)
    count = cursor.fetchall()[0][0]
    if count == 0:
        field = str('(name,time,type,title,context,project_id)')
        sql = 'insert into data_event' + field + " values(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,
                       (data['name'], data["time"], data["type"], data["title"], data['context'], data['project_id']))
    else:
        sql = "update data_event set type='%s', title='%s', context='%s' where project_id='%s' and time='%s'" % (
            data["type"], data['title'], data['context'], data["project_id"], data["time"])
        cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    response = JsonResponse({"data": 0, 'event': True})
    # pass
    return response


# 离在线数据范围更新
def db_range(request):
    new_range = request.POST.getlist('new_range[]')
    db_type = request.POST.get('db_type')
    db = pymysql.connect('127.0.0.1', 'root', '123456', 'db2')  # 连接数据库
    cursor = db.cursor()  # 创建游标
    if db_type == 'on':
        sql1 = 'update on_range set ' + new_range[1] + ' = ' + new_range[2] + ' where chars ="' + new_range[0] + '"'
    else:
        sql1 = 'update off_range set ' + new_range[1] + ' = ' + new_range[2] + ' where chars ="' + new_range[0] + '"'
    cursor.execute(sql1)  # 执行SQL语句
    db.commit()
    db.close()  # 关闭连接
    response = JsonResponse({"data": 0})
    return response


# 返回实时离/在线数据
def online_data(request):
    # print(request.META)
    the_type = request.POST.get('type')
    the_name = request.POST.get('name')
    a = dict(list(DataProject.objects.values_list('name', 'id'))).get(the_name)  # 获取项目id
    if the_type == 'on':
        last = request.POST.get("last")
        db = pymysql.connect('127.0.0.1', 'root', '123456', 'db2')  # 连接数据库
        cursor = db.cursor()  # 创建游标

        # 第一次访问数据
        if len(last) == 0:
            sql1 = "select *,unix_timestamp(SAMPLE_TIME)  from data_online where PROJECT_id=" + str(a)
        else:
            # 秒数 ,5个小时
            time_length = 6 * 60 * 60
            last2 = int(last) + time_length
            sql1 = "select *,unix_timestamp(SAMPLE_TIME)  from data_online where PROJECT_id=" + str(
                a) + " and unix_timestamp(sample_time) > " + str(last) + " and unix_timestamp(sample_time) <= " + str(
                last2)
            # SQL语句
        # b= DataOnline.objects.filter(project_id=a).values_list()
        # print(b)
        # print(sql1)
        cursor.execute(sql1)  # 执行SQL语句
        data = cursor.fetchall()  # 查询到所有的数据存储到all_users中
        cursor.close()
        db.close()
        response = JsonResponse(data, safe=False)
    else:
        event = list(DataEvent.objects.filter(name=the_name).values())
        server_data = list(DataOffline.objects.filter(PROJECT_id=a).values_list())
        response = JsonResponse({'event': event, "for": server_data})

    return response


def pagerange(request):
    # print(request.POST)
    data = request.POST.getlist("data[]")
    print(data)
    # 项目id
    pro_id = data[0]
    # 图表类型
    vtype = data[1]
    # max/min
    thetype = data[2]
    # 字段名称
    field = data[3]
    # 更改值
    value = data[4]
    if vtype == "on":
        if thetype == "max":
            ranges = Onrangemax
        else:
            ranges = Onrangemin
    else:
        if thetype == "max":
            ranges = Offrangemax
        else:
            ranges = Offrangemin
    s = {field.lower(): value}
    # print(s)
    ranges.objects.filter(project_id=pro_id).update(**s)
    return JsonResponse({"pro_on_data": 1})


# 获取所有的离线数据及离线事件
def get_offdata(request):
    pro_id = request.POST["pro_id"]
    # data = list(DataOffline.objects.filter(PROJECT_id=pro_id).values_list())
    db = pymysql.connect('127.0.0.1', 'root', '123456', 'db2')  # 连接数据库
    cursor = db.cursor()  # 创建游标
    # 获取所有离线数据
    sql1 = "select *,unix_timestamp(SAMPLE_TIME)  from data_offline where PROJECT_id=" + str(pro_id)
    cursor.execute(sql1)  # 执行SQL语句
    data = cursor.fetchall()  # 查询到所有的数据存储到data中
    cursor.close()
    db.close()
    event = list(DataEvent.objects.filter(project_id=pro_id).values_list())
    return JsonResponse({"data": data, 'event': event})
