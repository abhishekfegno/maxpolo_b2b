from rest_framework import serializers

from apps.order.models import SalesOrder
from apps.payment.models import Transaction
from lib.utils import get_local_time


class TransactionListSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return get_local_time(instance.created_at)

    def get_id(self, instance):
        return instance.order.id

    def get_order(self, instance):
        if instance.order:
            return {
                "order": instance.order.invoice_id,
                "actual_amount": instance.order.invoice_amount,
                "remaining_amount": instance.order.invoice_remaining_amount,
                "invoice_status": instance.order.invoice_status
            }
        else:
            return None

    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()


    def get_created_at(self, instance):
        return get_local_time(instance.created_at)

    # def get_order(self, instance):
    #     return {
    #         "order": instance.order.invoice_id,
    #         "actual_amount": instance.order.invoice_amount,
    #         "remaining_amount": instance.order.invoice_remaining_amount,
    #         "invoice_status": instance.order.invoice_status
    #     }

    class Meta:
        model = Transaction
        fields = ('amount', 'amount_balance', 'status', 'created_at')


class CreditListSerializer(serializers.ModelSerializer):
    transaction_set = TransactionSerializer(many=True)
    invoice_date = serializers.SerializerMethodField()

    def get_invoice_date(self, instance):
        return get_local_time(instance.invoice_date)

    class Meta:
        model = SalesOrder
        fields = ('id', 'invoice_id', 'invoice_amount', 'invoice_remaining_amount',
                  'invoice_status', 'invoice_date', 'transaction_set')
