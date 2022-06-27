from django_filters import FilterSet

from apps.catalogue.models import Product
from apps.order.models import SalesOrder
from apps.payment.models import Transaction
from apps.user.models import Complaint


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {'product_code': ['icontains'], 'name': ['icontains'], 'brand__name': ['icontains']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['product_code__icontains'].label = 'Product Code'
        self.filters['name__icontains'].label = 'Name'
        self.filters['brand__name__icontains'].label = 'Brand'


class OrderFilter(FilterSet):
    class Meta:
        model = SalesOrder
        fields = {'order_id': ['icontains'], 'dealer__username': ['icontains']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['order_id__icontains'].label = 'Order Id'
        self.filters['dealer__username__icontains'].label = 'Dealer'


class PaymentFilter(FilterSet):
    class Meta:
        model = Transaction
        fields = {'order__invoice_id': ['icontains'], 'status': []}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['order__invoice_id__icontains'].label = 'Invoice Id'


class ComplaintFilter(FilterSet):
    class Meta:
        model = Complaint
        fields = ('status', )

