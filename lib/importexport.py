from import_export import resources

from apps.order.models import SalesOrder
from apps.payment.models import Transaction
from apps.user.models import Complaint, Dealer


class OrderReport(resources.ModelResource):
    def __init__(self):
        super().__init__()
        self.fields['dealer'].queryset = Dealer.objects.all().values('username')


    class Meta:
        model = SalesOrder
        export_order = ('id', 'order_id', 'dealer', 'created_at')


class SalesOrderReport(resources.ModelResource):
    class Meta:
        model = SalesOrder
        export_order = ('id', 'order_id', 'dealer__username', 'is_confirmed', 'confirmed_date', 'created_at')


class InvoiceReport(resources.ModelResource):
    class Meta:
        model = SalesOrder
        export_order = ('id', 'order_id', 'invoice_id', 'dealer__username', 'is_confirmed', 'confirmed_date',
                        'invoice_date', 'invoice_amount', 'invoice_remaining_amount', 'created_at')


class ComplaintReport(resources.ModelResource):
    class Meta:
        model = Complaint


class PaymentReport(resources.ModelResource):
    class Meta:
        model = Transaction
