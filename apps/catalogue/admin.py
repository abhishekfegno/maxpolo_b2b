from django.contrib import admin

# Register your models here.
from apps.catalogue.models import *

admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Category)
