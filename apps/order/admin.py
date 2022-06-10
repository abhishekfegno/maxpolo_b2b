from django.contrib import admin

# Register your models here.
from apps.order.models import *

admin.site.register(SalesOrder)
admin.site.register(SalesOrderLine)
