from rest_framework import serializers

from apps.payment.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField()

    def get_order(self, instance):
        return {
            "order": instance.order.invoice_id,
            "actual_amount": instance.order.invoice_amount,
            "remaining_amount": instance.order.invoice_remaining_amount,
            "invoice_status": instance.order.invoice_status
        }

    class Meta:
        model = Transaction
        fields = '__all__'
