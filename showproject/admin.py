from django.contrib import admin

from .models import *


class DataProjectAdmin(admin.ModelAdmin):
    readall = DataProject.objects.all().values()
    keynames = readall[0].keys()
    list_display = list(keynames)


class DataOfflineAdmin(admin.ModelAdmin):
    readall = DataOffline.objects.all().values()
    keynames = readall[0].keys()
    list_display = list(keynames)


class DataOnlineAdmin(admin.ModelAdmin):
    readall = DataOnline.objects.all().values()
    keynames = readall[0].keys()
    list_display = list(keynames)


admin.site.register(DataOffline, DataOfflineAdmin)
admin.site.register(DataOnline, DataOnlineAdmin)
admin.site.register(DataProject, DataProjectAdmin)
# Register your models here.
