from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from apps.user.models import *


@admin.register(User)
class UserCustomAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'user_role', 'branch', 'mobile')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'user_role']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']


admin.site.register(Dealer)
admin.site.register(Executive)
admin.site.register(Complaint)
