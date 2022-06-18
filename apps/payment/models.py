from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.order.models import SalesOrder

#
# class Credit(models.Model):
#     order = models.ForeignKey('order.SalesOrder', on_delete=models.SET_NULL, null=True, blank=False)
#     amount_credited = models.FloatField(default=0.0)
#     amount_remaining = models.FloatField(default=0.0)
#     created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    order = models.ForeignKey('order.SalesOrder', on_delete=models.SET_NULL, null=True, blank=False)
    amount = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order.invoice_id


@receiver(post_save, sender=Transaction)
def invoice_amount_update(sender, created, instance, **kwargs):
    if created:
        actual_inv_amount = instance.order.invoice_amount
        paid_amount = instance.amount
        if paid_amount == actual_inv_amount:
            SalesOrder.objects.filter(pk=instance.order.pk).update(invoice_status='payment_done')
        elif paid_amount < actual_inv_amount:
            balance = actual_inv_amount - paid_amount
            print(f"balance:{balance},paid:{paid_amount}")
            SalesOrder.objects.filter(pk=instance.order.pk).update(invoice_status='Payment Partial',
                                                                   invoice_remaining_amount=balance)
