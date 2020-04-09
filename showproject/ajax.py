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


def his_field(request):
    name = request.POST.get('field')  # 获得选取的字段信息
    the_type = request.POST.get('the_type')  # 获取字段类型
    pro_name = request.POST.get("pro_name")
    pro_id = DataProject.objects.filter(name=pro_name).values_list("id", flat=True)[0]
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


# ajax历史参数聚类


def his_pro(request):
    # pro_name_id = dict(list(DataProject.objects.values_list('name', 'id')))
    print(request.POST)
    pro_id = request.POST.get('pro_id')
    field = request.POST.getlist("field")
    the_type = request.POST.get('the_type')
    # field.append('sampletime')
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
    # 获取范围
    # data = request.POST.getlist('data')  # 获得复选框中的项目及字段
    # the_type = request.POST.get('the_type')
    # gap = float(request.POST.get('gap'))
    # t = request.POST.getlist('the_range')
    # event = events(data[0], gap)
    # the_range = []
    # for i in range(0, len(t), 2):
    #     the_range.append([float(t[i]), float(t[i + 1])])
    # # print(data)
    # pro_data = search_return(pro_name_id.get(data[0]), data, the_type, gap, the_range)
    # response = JsonResponse({"pro_data": pro_data, 'event': event})
    response = JsonResponse({}, safe=False)
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


# 单图表数据范围选择
def page_range(request):
    the_range = request.POST.getlist('the_range[]')
    the_type = request.POST.get('type')
    the_length = float(request.POST.get('date_length'))
    t = [float(the_range[2]), float(the_range[3])]
    the_data = DataOnline
    if the_type == 'off':
        the_data = DataOffline
    pro_id = dict(list(DataProject.objects.values_list('name', 'id'))).get(the_range[0])
    data = list(the_data.objects.filter(PROJECT_id=pro_id).values_list(the_range[1], flat=True))
    re_time = list(the_data.objects.filter(PROJECT_id=pro_id).values_list('RELATIVETIME', flat=True))
    a = [None] * (int(max(re_time) / the_length) + 1)
    for indexj, j in enumerate(re_time):
        a[int(j / the_length)] = data[indexj]
    totaldata = none_dispose(a)
    data = one_data_rate(totaldata, t)
    response = JsonResponse({"data": data})
    return response


# 返回实时离/在线数据
def online_data(request):
    # print(request.META)
    the_type = request.POST.get('type')
    the_name = request.POST.get('name')
    a = dict(list(DataProject.objects.values_list('name', 'id'))).get(the_name)  # 获取项目id
    if the_type == 'on':
        last = request.POST.get("last")
        # print(last)
        # print(type(last))
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
        # print(sql1)
        cursor.execute(sql1)  # 执行SQL语句
        data = cursor.fetchall()  # 查询到所有的数据存储到all_users中
        cursor.close()
        db.close()
        response = JsonResponse(data, safe=False)

        # response = JsonResponse({"for": data})  # 返回未处理数据0
        # print(data)
        # response = HttpResponse(data)
    else:
        event = list(DataEvent.objects.filter(name=the_name).values())
        server_data = list(DataOffline.objects.filter(PROJECT_id=a).values_list())
        response = JsonResponse({'event': event, "for": server_data})

    return response


def on_field(request):
    the_type = request.POST.get('type')
    field_name = request.POST.get('name')
    gap = float(request.POST.get('gap'))
    update_pro = list(DataProject.objects.filter(update_flag=1).values_list('name', flat=True))
    update_pro.insert(0, field_name)
    if the_type == 'on':
        data = field_search([update_pro], 'on', gap)
    else:
        data = field_search([update_pro], 'off', gap)
    response = JsonResponse({"data": data[0]})
    return response
    # 实时参数聚类


def same_page(request):
    # pro_name_id = dict(list(DataProject.objects.values_list('name', 'id')))
    the_name = request.POST.get('pro_name')
    data_on = request.POST.getlist('data_on')
    data_off = request.POST.getlist('data_off')
    gap = float(request.POST.get('gap'))
    on_range = request.POST.getlist('on_range')
    off_range = request.POST.getlist('off_range')
    # print(on_range)
    # print(off_range)
    on_ranges = []
    off_ranges = []
    # pro_name_id = get_pro_name_id()
    for i in range(0, len(on_range), 2):
        on_ranges.append([float(on_range[i]), float(on_range[i + 1])])
    for i in range(0, len(off_range), 2):
        off_ranges.append([float(off_range[i]), float(off_range[i + 1])])
    pro_on_data = search_return(pro_name_id.get(data_on[0]), data_on, 'on', gap, on_ranges)
    pro_off_data = search_return(pro_name_id.get(data_off[0]), data_off, 'off', gap, off_ranges)
    response = JsonResponse({"pro_on_data": pro_on_data, 'pro_off_data': pro_off_data})

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
