from django import forms

from apps.order.models import SalesOrder
from apps.payment.models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('order', 'amount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order'].queryset = SalesOrder.objects.filter(is_invoice=True, invoice_status='credit').exclude(invoice_status='payment_done')
