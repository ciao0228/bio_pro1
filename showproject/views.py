# 此文件用于发送页面

from django.http import HttpResponseRedirect
from showproject.models import *
from django.shortcuts import render
from showproject.connect import *
import datetime
from django.views.decorators.clickjacking import xframe_options_exempt



@xframe_options_exempt
def view_render(request, html_name):
    if "uname" not in request.session:
        return HttpResponseRedirect('/login')

    if "name" in request.GET:
        name = request.GET["name"]
    else:
        updating = list(DataProject.objects.filter(update_flag=1).values("name", "begin_time"))  # 正在更新项目
        if len(updating) > 0:
            return HttpResponseRedirect('?name=' + updating[0]["name"])
    state = get_state()
    uploads = list(DataProject.objects.values_list('upload', flat=True).distinct())
    upload_id = request.GET.get('upload_id') if request.GET.get('upload_id') else '1'
    pro_names = list(DataProject.objects.filter(update_flag=None).values_list('name', flat=True))  # 获得所有项目名
    offs = list(OffRange.objects.values('chars', 'meaning', 'min', 'max'))  # 离线参数名,范围
    ons = list(OnRange.objects.values('chars', 'meaning', 'min', 'max'))  # 在线参数名，范围
    update_pro = list(DataProject.objects.filter(update_flag=1).values_list('name', flat=True))  # 正在更新项目
    updating = list(DataProject.objects.filter(update_flag=1).values("name", "begin_time"))  # 正在更新项目

    # print(time.mktime(updating[0].timetuple()))
    style = ['Solid', 'ShortDash', 'ShortDot', 'ShortDashDot', 'ShortDashDotDot', 'Dot', 'Dash', 'LongDash', 'DashDot',
             'LongDashDot', 'LongDashDotDot']
    print(datetime.datetime.now())
    for index in range(len(updating)):
        updating[index]["begin_time"] = time.mktime(updating[index]["begin_time"].timetuple())
        # time.mktime(dtime.timetuple())
        # updating[index] = list(updating[index])
        # updating[index] = time.mktime(updating[index].timetuple())
        # print(time.mktime(i[-1].timetuple()))
    print(updating)
    pro_id = list(DataProject.objects.values_list('id', flat=True))
    off_names = list(OffRange.objects.values_list('chars', flat=True))
    on_names = list(OnRange.objects.values_list('chars', flat=True))
    on_ranges = list(OnRange.objects.defer('id').values())
    off_ranges = list(OffRange.objects.values_list('chars', 'meaning', 'min', 'max'))

    return render(request, html_name, locals())


def history_pro(request):
    if "uname" not in request.session:
        return HttpResponseRedirect('/login')
    state = get_state()
    uploads = list(DataProject.objects.values_list('upload', flat=True).distinct())
    upload_id = request.GET.get('upload_id') if request.GET.get('upload_id') else '1'
    # 获得所有未在更新项目名
    pro_names = list(DataProject.objects.filter(update_flag=None).values('name', 'begin_time', 'id'))
    offs = list(OffRange.objects.values('chars', 'meaning', 'min', 'max'))  # 离线参数名,范围
    ons = list(OnRange.objects.values('chars', 'meaning', 'min', 'max'))  # 在线参数名，范围

    # print(time.mktime(updating[0].timetuple()))
    style = ['Solid', 'ShortDash', 'ShortDot', 'ShortDashDot', 'ShortDashDotDot', 'Dot', 'Dash', 'LongDash', 'DashDot',
             'LongDashDot', 'LongDashDotDot']
    print(datetime.datetime.now())
    pro_id = list(DataProject.objects.values_list('id', flat=True))
    off_names = list(OffRange.objects.values_list('chars', flat=True))
    on_names = list(OnRange.objects.values_list('chars', flat=True))
    on_ranges = list(OnRange.objects.defer('id').values())
    off_ranges = list(OffRange.objects.values_list('chars', 'meaning', 'min', 'max'))
    return render(request, 'history_pro.html', locals())


def history_fields(request):
    if "uname" not in request.session:
        return HttpResponseRedirect('/login')
    state = get_state()
    uploads = list(DataProject.objects.values_list('upload', flat=True).distinct())
    upload_id = request.GET.get('upload_id') if request.GET.get('upload_id') else '1'
    # 获得所有未在更新项目名
    pro_names = list(DataProject.objects.filter(update_flag=None).values('name', 'begin_time', 'id'))
    offs = list(OffRange.objects.values('chars', 'meaning', 'min', 'max'))  # 离线参数名,范围
    ons = list(OnRange.objects.values('chars', 'meaning', 'min', 'max'))  # 在线参数名，范围

    # print(time.mktime(updating[0].timetuple()))
    style = ['Solid', 'ShortDash', 'ShortDot', 'ShortDashDot', 'ShortDashDotDot', 'Dot', 'Dash', 'LongDash', 'DashDot',
             'LongDashDot', 'LongDashDotDot']
    print(datetime.datetime.now())
    pro_id = list(DataProject.objects.values_list('id', flat=True))
    off_names = list(OffRange.objects.values_list('chars', flat=True))
    on_names = list(OnRange.objects.values_list('chars', flat=True))
    on_ranges = list(OnRange.objects.defer('id').values())
    off_ranges = list(OffRange.objects.values_list('chars', 'meaning', 'min', 'max'))
    return render(request, 'history_fields.html', locals())


def layout(request):
    return view_render(request, 'layout.html')


def upload(request):
    return view_render(request, 'upload.html')


def online_pro(request):
    return view_render(request, 'online_pro.html')


def online_field(request):
    # 判断是否登录
    if "uname" not in request.session:
        return HttpResponseRedirect('/login')
    if "type" not in request.GET:
        if 'field' not in request.GET:
            return HttpResponseRedirect('/online_field?type=on&&field=TEMP')
    # 字段名
    # field = request.GET("field") if "field" in request.GET else field = ''
    the_type = request.GET['type']
    field = request.GET['field'].lower()
    style = ['Solid', 'ShortDash', 'ShortDot', 'ShortDashDot', 'ShortDashDotDot', 'Dot', 'Dash', 'LongDash', 'DashDot',
             'LongDashDot', 'LongDashDotDot']
    offs = list(OffRange.objects.values('chars', 'meaning', 'min', 'max'))  # 离线参数名,范围
    ons = list(OnRange.objects.values('chars', 'meaning', 'min', 'max'))  # 在线参数名，范围
    pro_names = list(DataProject.objects.filter(update_flag=None).values_list('name', flat=True))  # 获得所有项目名
    off_names = list(OffRange.objects.values_list('chars', flat=True))
    on_names = list(OnRange.objects.values_list('chars', flat=True))
    update_pro = list(DataProject.objects.filter(update_flag=1).values_list('name', flat=True))  # 正在更新项目
    updating = list(DataProject.objects.filter(update_flag=1).values("name", "begin_time", 'id'))  # 正在更新项目
    for index in range(len(updating)):
        updating[index]["begin_time"] = time.mktime(updating[index]["begin_time"].timetuple())
    if the_type == 'on':
        field_name = OnRange.objects.filter(chars=field.upper()).values_list('meaning', flat=True)[0]
        for i in updating:
            i['min'] = list(Onrangemin.objects.filter(project_id=i['id']).values_list(field, flat=1))[0]
            i['max'] = list(Onrangemax.objects.filter(project_id=i['id']).values_list(field, flat=1))[0]
    else:
        field_name = OffRange.objects.filter(chars=field.upper()).values_list('meaning', flat=True)[0]
        for i in updating:
            i['min'] = list(Offrangemin.objects.filter(project_id=i['id']).values_list(field, flat=1))[0]
            i['max'] = list(Offrangemax.objects.filter(project_id=i['id']).values_list(field, flat=1))[0]
    print(updating)
    return render(request, 'online_field.html', locals())


def container(request):
    if "uname" not in request.session:
        return HttpResponseRedirect('/login')
    if "name" in request.GET:
        # print(request.GET["name"])
        name = request.GET["name"]
        # 获取项目id
        # pro_id = dict(list(DataProject.objects.values_list('name', 'id'))).get(request.GET["name"])
        pro_id = DataProject.objects.filter(name=name).values_list("id",flat=1)[0]
        pro = DataProject.objects.filter(name=name).values()[0]
        print(pro)
        # 查找表中大小范围
        onmin = list(Onrangemin.objects.filter(project_id=pro_id).defer("project_id").values())[0]
        onmin.pop('project_id')
        onmax = list(Onrangemax.objects.filter(project_id=pro_id).defer("project_id").values())[0]
        onmax.pop("project_id")
        offmin = list(Offrangemin.objects.filter(project_id=pro_id).defer("project_id").values())[0]
        offmin.pop('project_id')
        offmax = list(Offrangemax.objects.filter(project_id=pro_id).defer("project_id").values())[0]
        offmax.pop("project_id")

        # 合并 范围参数[英文，中文，最大值，最小值]
        off = list(OffRange.objects.values_list('chars', 'meaning'))
        for i in range(len(off)):
            off[i] = {'chars': off[i][0], "meaning": off[i][1],
                      "max": offmax[off[i][0].lower()], "min": offmin[off[i][0].lower()]}
        on = list(OnRange.objects.values_list('chars', 'meaning'))
        for i in range(len(on)):
            on[i] = {"chars": on[i][0], "meaning": on[i][1],
                     "max": onmax[on[i][0].lower()], "min": onmin[on[i][0].lower()]}

    # print(request.GET)

    return render(request, "container.html", locals())


# def login(request):
#     print(request.session)
#     if request.method == "GET":
#         # 判断客户端是否有储存cookie
#         print(request.COOKIES)
#         if "login" in request.COOKIES:
#             login = request.COOKIES.get('login', '').split(',')
#             # cookies加密
#             # login = request.get_signed_cookie('login', '', salt='hello').split(',')
#             print(login)
#             # 用户名
#             uname = login[0]
#             # 密码
#             pwd = login[1]
#             return render(request, 'login.html', {"uname": uname, "pwd": pwd})
#         return render(request, 'login.html', {"uname": '', "pwd": ''})
#     else:
#         uname = request.POST.get("uname", "")
#         pwd = request.POST.get("pwd", "")
#         response = HttpResponse()
#         print(request.POST)
#         print(uname)
#         print(pwd)
#         # 判断登录是否成功
#         if uname == 'admin' and pwd == 'admin ':
#             response.content = "登录成功"
#             # 保存cookies
#             # response.set_signed_cookie("login", uname + ',' + pwd+';', "/login/", max_age=24 * 60 * 60 * 10)
#             response.set_cookie("login", uname + ',' + pwd, path="/login/", max_age=24 * 60 * 60 * 10)
#             # return render(request, 'login.html', {"uname": uname, "pwd": pwd})
#             return response
#
#         response.delete_cookie('login', '/login/')
#         return HttpResponse("登录失败")


def login(request):
    message = "请先登录"
    if request.method == "GET":
        # uname = request.session.get('uname', '')
        # pwd = request.session.get('pwd', '')
        if 'uname' in request.session:
            return HttpResponseRedirect('/online_pro')
        else:
            print(1)
            return render(request, 'login.html', {"uname": '', "pwd": '', "message": message})
    else:
        # print(2)
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', "")
        # 判断用户名密码是否匹配
        if uname == "uname" and pwd == "123456":
            request.session['uname'] = uname
            return HttpResponseRedirect('/online_pro')
        else:
            message = "用户名或密码不正确"
            # print(message)
            return render(request, 'login.html', {"message": message})


def exits(request):
    # 清除session
    request.session.clear()
    request.session.flush()
    # print(request.session['uname'])
    return HttpResponseRedirect('/login')


def register(request):
    if request.method == 'POST':
        message = request.POST
        user = list(User1.objects.filter(username=message['uname']).values_list())
        # print(len(user))
        if len(user) != 0:
            return HttpResponse("该账户已注册！")
        # print(user)
        request.session.clear()
        request.session.flush()
        return HttpResponseRedirect('/login')
    else:
        # print(request.POST)
        return render(request, 'register.html')

def c(request):
    return JsonResponse({"cat":"cat"})