from django.conf.urls import url

from . import views, ajax

app_name = 'showproject'

urlpatterns = [
    url(r'^c$', views.c),
    url(r'^layout', views.layout),
    url(r'^upload', views.upload),  # 测试页面
    url(r'^history_fields', views.history_fields),
    url(r'^history_pro', views.history_pro),
    url(r'^online_field', views.online_field),
    url(r'^online_pro', views.online_pro),
    url(r'^exits', views.exits),

    # 数据范围设置
    url(r'^login', views.login),
    url(r'^db_range/', ajax.db_range),
    # 实时数据交互
    url(r'^create/', ajax.create),
    url(r'^open_close/', ajax.open_close),
    url(r'^event_values/', ajax.event_values),
    url(r'^online_data/', ajax.online_data),
    # 历史数据
    url(r'^field_data/', ajax.field_data),
    url(r'^his_field/', ajax.his_field),
    url(r'^his_pro/', ajax.his_pro),

    url(r"^container", views.container),
    url(r"^pagerange", ajax.pagerange),
    url(r"^get_offdata", ajax.get_offdata),
    url(r'^save_values/', ajax.save_values),
    

]
