from django.contrib import admin

# Register your models here.

from apps.executivetracking.models import *


admin.site.register(CheckPoint)
admin.site.register(CrashReport)

