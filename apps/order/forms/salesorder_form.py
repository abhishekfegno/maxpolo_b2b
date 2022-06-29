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
    # order_id = forms.CharField(required=False,
    # 	widget=forms.TextInput(attrs={'readonly': 'readonly'})
    # )

    class Meta:
        model = SalesOrder
        fields = ('is_confirmed', 'is_cancelled')
        labels = {
            'is_confirmed': 'Confirm this order ?',
            'is_cancelled': 'Cancel this order ?'
        }


class SalesOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ('is_invoice',)
        labels = {
            'is_invoice': 'Invoice this order ?',
        }


class InvoiceUpdateForm(forms.ModelForm):
    # invoice_status = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # invoice_amount = forms.FloatField(required=False)

    class Meta:
        model = SalesOrder
        fields = ('invoice_status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False


class InvoiceAmountForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ('invoice_amount',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False
