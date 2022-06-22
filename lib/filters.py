from django_filters import FilterSet

from apps.catalogue.models import Product
from apps.order.models import SalesOrder
from apps.payment.models import Transaction


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {'product_code': ['icontains'], 'name': ['icontains'], 'brand__name': ['icontains']}


class OrderFilter(FilterSet):
    class Meta:
        model = SalesOrder
        fields = {'order_id': ['icontains'], 'dealer__username': ['icontains']}


class PaymentFilter(FilterSet):
    class Meta:
        model = Transaction
        fields = {'order__invoice_id': ['icontains'], 'status': []}
