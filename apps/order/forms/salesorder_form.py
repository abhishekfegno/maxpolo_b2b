# New file created 
from django import forms

from apps.order.models import SalesOrder, SalesOrderLine


class QuotationForm(forms.ModelForm):
	class Meta:
		model = SalesOrder
		fields = ('dealer',)


class QuotationLineForm(forms.ModelForm):
	class Meta:
		model = SalesOrderLine
		fields = ('product', 'quantity')


class QuotationUpdateForm(forms.ModelForm):
	class Meta:
		model = SalesOrder
		fields = ('order_id', 'is_confirmed', 'is_cancelled', 'is_invoice')


class SalesOrderUpdateForm(forms.ModelForm):
	class Meta:
		model = SalesOrder
		fields = ('is_confirmed', 'is_cancelled', 'is_invoice')


class InvoiceUpdateForm(forms.ModelForm):
	class Meta:
		model = SalesOrder
		fields = ('is_confirmed', 'is_cancelled', 'is_invoice')
