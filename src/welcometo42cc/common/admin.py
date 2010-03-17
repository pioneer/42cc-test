from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from common.models import HttpRequestLogRecord, ModelLog


UserAdmin.fieldsets += (
    ('Extra info', {'fields': ('biography', 'birthdate', 'contacts')}),
    )


class HttpRequestLogRecordAdmin(admin.ModelAdmin):
    list_display = ('url', 'status_code', 'datetime')

admin.site.register(HttpRequestLogRecord, HttpRequestLogRecordAdmin)


class ModelLogAdmin(admin.ModelAdmin):
    pass

admin.site.register(ModelLog, ModelLogAdmin)
