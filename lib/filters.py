from django_filters import FilterSet

from apps.catalogue.models import Product
from apps.order.models import SalesOrder


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = ('product_code', 'name', 'brand')



class OrderFilter(FilterSet):
    class Meta:
        model = SalesOrder
        fields = ('order_id', 'is_cancelled')


# class InvoiceFilter(FilterSet):
#     class Meta:
#         model = SalesOrder
#         fields = ('product_code', 'name', '')