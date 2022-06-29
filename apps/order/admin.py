from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from apps.order.models import *
from lib.importexport import OrderReport


class SalesOrderAdmin(ImportExportModelAdmin):
    resource_class = OrderReport


admin.site.register(SalesOrder, SalesOrderAdmin)
admin.site.register(SalesOrderLine)
