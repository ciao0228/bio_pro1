# 此文件用于数据处理

from showproject.models import *
import time


# pro_name_id = get_pro_name_id()


def transpose(matrix):
    new_matrix = []
    for matrixi in range(len(matrix[0])):
        matrix1 = []
        for matrixj in range(len(matrix)):
            matrix1.append(matrix[matrixj][matrixi])
        new_matrix.append(matrix1)
    return new_matrix


# 定义列表转置函数


def dict_en_cn(field):
    if field == 'on':
        return dict(OnRange.objects.values_list('chars', 'meaning'))
    else:
        return dict(OffRange.objects.values_list('chars', 'meaning'))


# 返回字段中英文对比

def get_pro_name_id():
    return list(DataProject.objects.values_list('name', 'id'))


# pro_name_id = dict(get_pro_name_id())


# 获得项目名和id

def one_data_rate1(matrix):
    new_matrix = []
    extremum = max(matrix) - min(matrix)  # 极值
    if extremum != 0:
        for i in matrix:
            new_matrix.append(
                float((i - min(matrix)) / extremum)
            )
        return new_matrix
    else:
        return matrix


# 定义计算百分比函数，输入一维数组，返回对应一维数组的百分占比

def one_data_rate(matrix, the_range):
    new_matrix = []
    extremum = the_range[1] - the_range[0]  # 极值
    if extremum != 0:
        for i in matrix:
            new_matrix.append(
                round(float((i - the_range[0]) / extremum), 6)
            )
        return new_matrix
    else:
        return matrix


# 定义计算百分比函数，输入一维数组，返回对应一维数组的百分占比


def data_rate(matrix, the_range):
    new_matrix = []
    for index, i in enumerate(matrix):
        new_matrix.append(
            one_data_rate(i, the_range[index])
        )
    return new_matrix


# 定义计算百分比函数，输入二维数组，返回对应二维数组的百分占比


def string_split(wait_string, split_string):
    s = []
    new_id = []
    if len(wait_string) != 0:
        for name_id in wait_string:
            n_id = name_id.split(split_string)
            new_id.append(
                list(n_id),
            )
        name = new_id[0][0]
        new = [name]
        for i in new_id:
            if name == i[0]:
                new.append(
                    i[1]
                )
            else:
                s.append(
                    new
                )
                name = i[0]
                new = i
        s.append(new)
    return s


# 接收待处理的一维字符串数组和分隔符，处理后返回分组后的二维数组


def none_dispose(field):
    a = 0  # 空值初始化
    return_field = []
    for i in field:
        if i is not None:
            a = i
        return_field.append(
            a
        )
    return return_field


# 对参数进行空值处理


def search_return(pro_id, mation, the_type='on', length=3600, the_range=[]):
    the_data = DataOnline
    the_datarange = OnRange
    # print(mation)
    if the_type == 'off':
        the_data = DataOffline
        the_datarange = OffRange
    name = mation.pop(0)
    # print(mation)
    # print(the_data.objects.filter(PROJECT_id=pro_id).values_list(*mation))
    if len(list(the_data.objects.filter(PROJECT_id=pro_id).values())) == 0:
        return list(the_datarange.objects.values_list('meaning'))
    else:

        # print(the_data.objects.filter(PROJECT_id=pro_id).values_list(*mation))
        readall = []
        for i in mation:
            readall.append(
                the_data.objects.filter(PROJECT_id=pro_id).values_list(i, flat=True)
            )
        # print(readall)
        if len(the_range) == 0:
            for i in mation:
                the_range.append(
                    list(the_datarange.objects.values_list('min', 'max').filter(chars=i))[0]
                )
        totaldata = []
        re_time = the_data.objects.filter(PROJECT_id=pro_id).values_list('RELATIVETIME', flat=True)
        for i in readall:
            a = [None] * (int(max(re_time) / length) + 1)
            for indexj, j in enumerate(re_time):
                a[int(j / length)] = i[indexj]
            totaldata.append(
                none_dispose(a)
            )  # 对参数进行空值处理
        data_time = [i for i in range(int(max(re_time) / length) + 1)]
        relative_time = ['RELATIVE_TIME', data_time]  # 记录相对时间
        total_data = data_rate(totaldata, the_range)  # 计算参数百分占比
        final_data = [[name, pro_id], relative_time]
        for index_k, k in enumerate(total_data):
            a = ["", k]
            # print(list(the_datarange.objects.filter(chars=mation[index_k]).values())[0])
            final_data.append(a)
        return final_data


# 定义函数，返回指定离在线项目名称，id，相对时间，字段信息


def field_deal(matrix, string_splits):
    a = []
    for i in matrix:
        a.append(
            i.split(string_splits)
        )
    a.sort(key=lambda x: x[1])
    b = []
    if len(a) != 0:
        field_name = a[0][1]
        alls = [field_name]
        for i in a:
            if i[1] == field_name:
                alls.append(
                    i[0]
                )
            else:
                b.append(
                    alls
                )
                field_name = i[1]
                alls = [field_name, i[0]]
        b.append(alls)
    return b


def field_search(field, the_type='on', the_length=3600):  # 输入二维数组，其中一维为单个字段名+所有项目名
    data = DataOnline
    field_range = OnRange
    if the_type == 'off':
        data = DataOffline
        field_range = OffRange
    # pro_name_id = get_pro_name_id()
    a = []
    for j in field:
        the_time = []
        name = j.pop(0)
        b = list(field_range.objects.filter(chars=name).values())
        for i in j:
            pro_id = dict(list(DataProject.objects.values_list('name', 'id'))).get(i)
            relative_time = data.objects.filter(PROJECT_id=pro_id).values_list('RELATIVETIME', flat=True)
            if len(relative_time) == 0:
                b.append(
                    [i, [0]]
                )
                continue
            the_time.append(
                max(list(relative_time))
            )
            d = list(
                data.objects.filter(PROJECT_id=pro_id).values_list('RELATIVETIME', name).order_by('RELATIVETIME'))
            e = [None] * (int(d[-1][0] / the_length) + 1)
            for indexk, k in enumerate(d):
                e[int(k[0] / the_length)] = k[1]
            e = one_data_rate1(none_dispose(e))
            b.append(
                [i, e]  # 添加项目名 ,数据
            )
        if len(the_time) == 0:
            b.insert(1, [0])
        else:
            matrix = [i for i in range(int(max(the_time) / the_length))]
            b.insert(1, matrix)
        a.append(
            b
        )
    return a


# 按照字段返回离\在线数据

def events(pro_name, gap):
    event = list(DataEvent.objects.filter(name=pro_name).values())
    if len(event) == 0:
        return 0
    begintime = list(DataProject.objects.filter(name=pro_name).values_list('begin_time', flat=True))[0]
    for i in event:
        i['re_time'] = float((time.mktime(i['time'].timetuple()) - time.mktime(begintime.timetuple())) / gap)
        i['time'] = time.strftime("%Y-%m-%d %H:%M:%S", i['time'].timetuple())
    return event


# 初始化设置项目范围
def setrange(cursor, pro_id):
    # 离线
    # 字段名
    name = list(OffRange.objects.values_list('chars', flat=True))
    names = "project_id"
    # 范围
    # 最小值
    ranges = list(OffRange.objects.values_list('min', flat=True))
    ranges.insert(0, pro_id)
    for i in name:
        names = names + ',' + i
    sql = "insert into offrangemin(" + names + ") values " + str(tuple(ranges))
    cursor.execute(sql)
    # 最大值
    ranges = list(OffRange.objects.values_list('max', flat=True))
    ranges.insert(0, pro_id)
    sql = "insert into offrangemax(" + names + ") values " + str(tuple(ranges))
    cursor.execute(sql)

    # 在线
    # 字段名
    name = list(OnRange.objects.values_list('chars', flat=True))
    names = "project_id"
    # 范围
    # 最小值
    ranges = list(OnRange.objects.values_list('min', flat=True))
    ranges.insert(0, pro_id)
    for i in name:
        names = names + ',' + i
    sql = "insert into onrangemin(" + names + ") values " + str(tuple(ranges))
    cursor.execute(sql)
    # 最大值
    ranges = list(OnRange.objects.values_list('max', flat=True))
    ranges.insert(0, pro_id)
    sql = "insert into onrangemax(" + names + ") values " + str(tuple(ranges))
    cursor.execute(sql)
