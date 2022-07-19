from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from apps import executivetracking
from apps.executivetracking.models import CheckPoint
from apps.order.models import SalesOrder
from apps.payment.models import Transaction
from apps.user.models import Complaint, Dealer, Executive


class OrderReport(resources.ModelResource):
    dealer = fields.Field(
        column_name='dealer',
        attribute='dealer',
        widget=ForeignKeyWidget(Dealer, 'username'))

    class Meta:
        model = SalesOrder
        export_order = ('id', 'order_id', 'dealer', 'created_at')


class SalesOrderReport(resources.ModelResource):
    dealer = fields.Field(
        column_name='dealer',
        attribute='dealer',
        widget=ForeignKeyWidget(Dealer, 'username'))

    class Meta:
        model = SalesOrder
        export_order = ('id', 'order_id', 'dealer', 'is_confirmed', 'confirmed_date', 'created_at')


class InvoiceReport(resources.ModelResource):
    dealer = fields.Field(
        column_name='dealer',
        attribute='dealer',
        widget=ForeignKeyWidget(Dealer, 'username'))

    class Meta:
        model = SalesOrder
        export_order = ('id', 'order_id', 'invoice_id', 'dealer', 'is_confirmed', 'confirmed_date',
                        'invoice_date', 'invoice_amount', 'invoice_remaining_amount', 'created_at')


class ComplaintReport(resources.ModelResource):
    class Meta:
        model = Complaint


class PaymentReport(resources.ModelResource):
    class Meta:
        model = Transaction


class DealerReport(resources.ModelResource):
    class Meta:
        model = Dealer
        export_order = ('first_name', 'mobile', 'email', 'company_cin', 'executive__first_name')


class ExecutiveReport(resources.ModelResource):
    class Meta:
        model = Executive
        export_order = ('first_name', 'mobile', 'email', 'company_cin', 'executive__first_name')


class CheckPointReport(resources.ModelResource):
    class Meta:
        model = CheckPoint
        export_order = ('store', 'check_in_at', 'description', 'location_text')
