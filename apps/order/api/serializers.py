from django.db.models import Sum
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
        return {
            "id": 0,
            "product_code": '',
            "product_name": '- Missing - '
        }

    class Meta:
        model = SalesOrderLine
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    line = OrderLineSerializer(many=True)
    dealer = serializers.SerializerMethodField()
    timeline = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    transaction = serializers.SerializerMethodField()

    def get_status(self, instance):
        return instance.status
    
    def get_dealer(self, instance):
        if instance.dealer:
            return {
                "id": instance.dealer_id,
                "name": instance.dealer.get_full_name()
            }

    def get_timeline(self, instance):
        if instance.dealer:
            last_transaction_date = None
            if instance.is_invoice:
                last_transaction = instance.transaction_set.all().exclude(status='cancelled').order_by('-id').first()
                last_transaction_date = last_transaction and last_transaction.created_at
            return {
                "new": {
                    "status": True,
                    "date": instance.created_at,
                    "label": "Placed",
                },
                "confirmed": {
                    "status": instance.is_invoice or instance.is_confirmed,
                    "date": instance.confirmed_date,
                    "label": "Confirmed",
                },
                "invoiced": {
                    "status": instance.is_invoice,
                    "date": instance.invoice_date,
                    "label": "Invoiced",
                },
                "completed": {
                    "status": instance.invoice_amount > 0 and instance.invoice_remaining_amount > 0,
                    "date": last_transaction_date,
                    "label": "Paid",
                },
            }

    def get_transaction(self, instance):
        return instance.transaction_set.all().values('amount', 'amount_balance', 'status', 'created_at').order_by('-id')

    class Meta:
        model = SalesOrder
        fields = ('id', 'order_id', 'invoice_id', 'invoice_status', 'invoice_date', 'invoice_amount',
                  'invoice_remaining_amount', 'confirmed_date', 'is_invoice', 'is_cancelled', 'is_confirmed',
                  'is_quotation', 'dealer', 'created_at', 'line', 'timeline', 'status', 'transaction')


class OrderLineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderLine
        fields = ('product', 'quantity')


class OrderCreateSerializer(serializers.ModelSerializer):
    line = OrderLineCreateSerializer(many=True)

    class Meta:
        model = SalesOrder
        fields = ('dealer', 'line', )

    def create(self, validated_data):
        lines = validated_data.pop('line')
        instance = SalesOrder.objects.create(dealer=validated_data['dealer'])
        if not instance.dealer:
            # import pdb;pdb.set_trace()
            instance.dealer = self.context.get('request').user
            instance.save()
        for line in lines:
            SalesOrderLine.objects.create(order=instance, product=line['product'], quantity=line['quantity'])
        return instance


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
