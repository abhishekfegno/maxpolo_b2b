from django.contrib import admin

# Register your models here.
from apps.user.models import *

admin.site.register(User)
admin.site.register(Dealer)
admin.site.register(Executive)
admin.site.register(Complaint)
