from django.contrib import admin

# Register your models here.

from .models import Project, DataRegion
from spider.driver.base.field import FieldName

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', FieldName.DATA_WEBSITE, FieldName.DATA_REGION, FieldName.DATA_SOURCE, 'status', 'created_time', 'modified_time', 'editor']

admin.site.register(Project, ProjectAdmin)
admin.site.register(DataRegion)