from django.contrib import admin
from .models import Statistic, DataItem

# Register your models here.
class statisticAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
admin.site.register(Statistic, statisticAdmin)


class dataItemAdmin(admin.ModelAdmin):
    list_display = ('statistic', 'owner', 'value',)
admin.site.register(DataItem, dataItemAdmin)
