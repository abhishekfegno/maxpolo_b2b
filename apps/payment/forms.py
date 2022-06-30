from django import forms

from apps.order.models import SalesOrder
from apps.payment.models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('order', 'amount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        so_qs = SalesOrder.objects.filter(
            is_invoice=True, invoice_status__in=['credit', 'payment_partial']).select_related('dealer')
        for s in so_qs:
            s.__show_dealer_in_str__ = True
            print(s)
        self.fields['order'].queryset = so_qs
