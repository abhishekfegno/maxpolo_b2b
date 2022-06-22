# New file created 
from django import forms
from django.forms import CheckboxInput

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
	# order_id = forms.CharField(required=False,
	# 	widget=forms.TextInput(attrs={'readonly': 'readonly'})
	# )

	class Meta:
		model = SalesOrder
		fields = ('is_confirmed', 'is_cancelled', 'is_invoice', 'is_quotation')
		# widgets = {
		# 	'is_confirmed': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
		# 	'is_cancelled': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
		# 	'is_invoice': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
		# }


class SalesOrderUpdateForm(forms.ModelForm):
	class Meta:
		model = SalesOrder
		fields = ('is_confirmed', 'is_invoice')


class InvoiceUpdateForm(forms.ModelForm):
	invoice_id = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

	class Meta:
		model = SalesOrder
		fields = ('invoice_id', 'is_invoice', 'invoice_status', 'invoice_amount', 'invoice_remaining_amount')
