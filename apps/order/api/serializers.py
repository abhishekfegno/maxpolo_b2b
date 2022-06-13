from rest_framework import serializers

from apps.catalogue.models import Product
from apps.order.models import SalesOrder, SalesOrderLine


class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderLine
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    line = OrderLineSerializer(many=True)

    class Meta:
        model = SalesOrder
        fields = '__all__'


