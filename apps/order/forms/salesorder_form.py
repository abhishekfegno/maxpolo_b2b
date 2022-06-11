# New file created 
from django import forms

from apps.order.models import SalesOrder


class SalesOrderForm(forms.ModelForm):
	class Meta:
		model = SalesOrder
		fields = '__all__'
