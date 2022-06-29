from rest_framework import serializers

from apps.order.models import SalesOrder, SalesOrderLine


class UpcomingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrder
        fields = ('id', 'invoice_id', 'invoice_date')


class OrderLineSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, instance):
        if instance.product:
            return {
                "id": instance.product_id,
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
        if instance.dealer:
            return {
                "id": instance.dealer_id,
                "name": instance.dealer.get_full_name()
            }

    class Meta:
        model = SalesOrder
        fields = ('id', 'order_id', 'invoice_id', 'invoice_status', 'invoice_date', 'invoice_amount',
                  'invoice_remaining_amount', 'confirmed_date', 'is_invoice', 'is_cancelled', 'is_confirmed',
                  'is_quotation', 'dealer', 'created_at', 'dealer', 'line')


class OrderDetailSerializer(serializers.ModelSerializer):
    line = OrderLineSerializer(many=True)
    dealer = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

    def get_dealer(self, instance):
        if instance.dealer:
            return {
                "id": instance.dealer_id,
                "name": instance.dealer.get_full_name()
            }

    def get_transactions(self, instance):
        return instance.transaction_set.all().values('amount', 'created_at')

    class Meta:
        model = SalesOrder
        fields = ('id', 'order_id', 'invoice_id', 'invoice_status', 'invoice_date', 'invoice_amount',
                  'invoice_remaining_amount', 'confirmed_date', 'is_invoice', 'is_cancelled', 'is_confirmed',
                  'is_quotation', 'dealer', 'created_at', 'dealer', 'line', 'transactions')
