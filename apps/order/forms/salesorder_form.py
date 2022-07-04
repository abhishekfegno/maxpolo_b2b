# New file created 
from django import forms

from apps.order.models import SalesOrder, SalesOrderLine


class QuotationForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ('dealer',)


class QuotationLineFormset():
    pass


class QuotationLineForm(forms.ModelForm):

    class Meta:
        model = SalesOrderLine
        fields = ('product', 'quantity')


class QuotationUpdateForm(forms.ModelForm):
    # order_id = forms.CharField(required=False,
    # 	widget=forms.TextInput(attrs={'readonly': 'readonly'})
    # )
    is_confirmed = forms.BooleanField(required=False)
    is_cancelled = forms.BooleanField(required=False)
    is_quotation = forms.BooleanField(required=False)
    invoice_id = forms.CharField(required=False)
    invoice_status = forms.CharField(required=False)
    invoice_amount = forms.FloatField(required=False)
    invoice_remaining_amount = forms.FloatField(required=False)
    confirmed_date = forms.DateField(required=False)
    invoice_date = forms.DateField(required=False)

    class Meta:
        model = SalesOrder
        fields = ('is_confirmed', 'is_cancelled', 'is_quotation', 'is_invoice', 'invoice_id',
                  'invoice_status', 'invoice_amount', 'invoice_remaining_amount',
                  'confirmed_date', 'invoice_date')


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


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ('dealer', 'invoice_amount', 'invoice_id')
