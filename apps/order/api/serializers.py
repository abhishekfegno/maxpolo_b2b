from rest_framework import serializers

from apps.catalogue.api.serializers import ProductSerializer
from apps.catalogue.models import Product
from apps.order.models import SalesOrder, SalesOrderLine



class OrderLineSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, instance):
        return {
            "product_code": instance.product.product_code,
            "product_name": instance.product.name
        }

    class Meta:
        model = SalesOrderLine
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    line = OrderLineSerializer(many=True)
    dealer = serializers.SerializerMethodField()

    def get_dealer(self, instance):
        return {
            "id": instance.dealer_id,
            "name": instance.dealer.get_full_name()
        }


    class Meta:
        model = SalesOrder
        fields = ('id', 'order_id', 'invoice_id', 'invoice_status', 'invoice_date', 'invoice_amount',
                  'invoice_remaining_amount', 'confirmed_date', 'is_invoice', 'is_cancelled', 'is_confirmed',
                  'is_quotation', 'dealer', 'created_at', 'dealer', 'line')
