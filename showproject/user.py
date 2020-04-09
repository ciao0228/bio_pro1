from django.contrib.auth.models import User
#
from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

# from django.http import JsonResponse

from django import forms

from django.forms import widgets

import re

####Form组件

class UserForm(forms.Form):    #必须继承Form
    user=forms.CharField(min_length=5,
                         label="用户名",
                         error_messages={"required":"用户名不能为空"},
                         # 想type=text的input标签添加个类
                         widget=widgets.TextInput(attrs={"placeholder":"请您输入用户名","class":"input"})
                         )
    pwd=forms.CharField(error_messages={"required":"密码不能为空"},
                        label="密码",
                        min_length=7,
                        widget=widgets.PasswordInput(attrs={"placeholder":"请您输入数字与字母组合的密码","class":"input"})
                        )
    r_pwd=forms.CharField(error_messages={"required":"密码不能为空"},
                          label="确认密码",
                          min_length=7,
                          widget=widgets.PasswordInput(attrs={"placeholder": "请您再次输入密码","class":"input"})
                          )
    email=forms.EmailField(required=True,
                           error_messages={"invalid":"邮箱格式错误",
                                           "required":"邮箱不能为空"},
                           label="邮箱",
                           widget=widgets.EmailInput(attrs={"placeholder": "请输入您的邮箱","class":"input"})
                           )

    # 局部钩子
    def clean_user(self):
        # 从第一层校验正确的{:}中取正确的用户名
        val=self.cleaned_data.get("user")
        user=User.objects.filter(username=val).first()
        if not user:
            return val
        else:
            raise ValidationError("用户名已存在!")


    def clean_pwd(self):
        val=self.cleaned_data.get("pwd")
        if val.isdigit():      #如果密码是纯数字
            raise ValidationError("密码不能是纯数字")    #传给错误{:}
        else:
            return val


    def clean_email(self):
        val=self.cleaned_data.get("email")
        if re.search("\w+@163.com$",val):
            return val
        else:
            raise ValidationError("邮箱必须是163邮箱！")


#     全局钩子
    def clean(self):                       #如果第一层没通过,空
        pwd=self.cleaned_data.get("pwd")
        r_pwd=self.cleaned_data.get("r_pwd")

        if pwd and r_pwd:     #如果全局钩子没有错误,发安徽null,有值,
            if pwd==r_pwd:    #结构相同,验证通过,返回正确 {:}
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一样")

        else:
            return self.cleaned_data

        # 另一个简便方法
        # if pwd and r_pwd and r_pwd != pwd:
        #     self.add_error("r_pwd", ValidationError("两次密码不一致！"))
        # else:
        #     return self.cleaned_data


# 注册
def zhuce(request):

    if request.method=="POST":

        form=UserForm(request.POST)
        print(form)

        res={"user":None,"err_msg":""}

        if form.is_valid():
            res["user"]=form.cleaned_data.get("user")
            print(form.cleaned_data)
            user=form.cleaned_data.get("user")
            pwd=form.cleaned_data.get("pwd")
            email=form.cleaned_data.get("email")
            user=User.objects.create_user(username=user,password=pwd,email=email)


        else:
            print(form.errors)
            print(form.cleaned_data)
            res["err_msg"]=form.errors

        return JsonResponse(res)

    else:
        form=UserForm()
        return render(request,"zhuce.html",locals())