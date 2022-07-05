# New file created 
from django import forms

from apps.order.models import SalesOrder, SalesOrderLine
from apps.payment.models import Transaction


class QuotationForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ('dealer',)


class TransactionCreateForm(forms.ModelForm):
    
    def __init__(self, *args, order, **kwargs):
        self.order: SalesOrder = order
        super(TransactionCreateForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        inv_number = self.order.id_as_text
        if self.cleaned_data['amount'] <= 0:
            raise forms.ValidationError(f"Invalid Amount. Amount must be greater than 0")
        if self.order.is_cancelled:
            raise forms.ValidationError(f"This Invoice is a cancelled {inv_number}")
        if not self.order.invoice_amount:
            raise forms.ValidationError(f"No invoice has been generated against {inv_number}")
        if self.order.invoice_remaining_amount < self.cleaned_data['amount']:
            raise forms.ValidationError(f"Could not mark Rs. {self.cleaned_data['amount']} ; since only Rs {self.order.invoice_remaining_amount} is remaining as credit")
        return self.cleaned_data
    
    def save(self, commit=True):
        self.instance.order = self.order
        self.instance.invoice_status = self.order

        self.instance = super().save(commit=commit)
        return self.instance

    class Meta:
        model = Transaction
        fields = ('amount', )


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
                  'confirmed_date', 'invoice_date', 'invoice_pdf')


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
        fields = ('invoice_amount', 'invoice_pdf')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ('dealer', 'invoice_amount', 'invoice_id', 'invoice_pdf')
