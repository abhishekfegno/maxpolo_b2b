from django.contrib import admin

# Register your models here.
from apps.payment.models import Transaction

admin.site.register(Transaction)
