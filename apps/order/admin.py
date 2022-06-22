from django.contrib import admin

# Register your models here.
from apps.order.models import *


from import_export.admin import ImportExportModelAdmin

from lib.importexport import OrderReport


class SalesOrderAdmin(ImportExportModelAdmin):
    resource_class = OrderReport


admin.site.register(SalesOrder, SalesOrderAdmin)
admin.site.register(SalesOrderLine)
