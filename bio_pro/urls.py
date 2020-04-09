"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpattepythrns:  url(r'^blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from showproject import views, ajax, connect, user

urlpatterns = [
                  path('', RedirectView.as_view(url='online_pro')),
                  # path('online_pro/', RedirectView.as_view(url='./online_pro')),
                  # 登录界面
                  url(r'^login', views.login),
                  # url(r'^', include('showproject.urls', namespace='showproject')),
                  url(r'^layout', views.layout),
                  url(r'^upload', views.upload),  # 测试页面
                  url(r'^history_fields', views.history_fields),
                  url(r'^history_pro', views.history_pro),
                  url(r'^online_field', views.online_field),
                  url(r'^online_pro', views.online_pro),
                  url(r'^exits', views.exits),
                  # url(r'^register/', views.register),
                  # url(r'^registers/', views.registers),
                  # path('login/', user.login),
                  # path('get_valid_img/', user.get_valid_img),
                  # path('zhuce/', user.zhuce),
                  # path('books/', user.book_view),

                  # 数据范围设置
                  url(r'^db_range/', ajax.db_range),
                  url(r'^page_range/', ajax.page_range),
                  # 实时数据交互
                  url(r'^create/', ajax.create),
                  url(r'^open_close/', ajax.open_close),
                  url(r'^event_values/', ajax.event_values),
                  url(r'^online_data/', ajax.online_data),
                  url(r'^on_field/', ajax.on_field),
                  # 历史数据
                  url(r'^field_data/', ajax.field_data),
                  url(r'^his_field/', ajax.his_field),
                  url(r'^his_pro/', ajax.his_pro),
                  url(r'^same_page/', ajax.same_page),

                  url(r'^connect', connect.connect),
                  url(r"^container", views.container),
                  url(r"^pagerange", ajax.pagerange),
                  url(r"^get_offdata", ajax.get_offdata),
                  url(r'^save_values/', ajax.save_values),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
