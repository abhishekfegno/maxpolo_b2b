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


class AmountMissMatchException(Exception):
    pass


class QuantityInvalidException(Exception):
    pass


class Transaction(models.Model):
    CHOICES = (
        ('new', 'New'),
        ('credit', 'Credit'),
        ('payment_partial', 'Payment Partial'),
        ('payment_done', 'Payment Done'),
        ('cancelled', 'Cancelled')
    )
    order = models.ForeignKey('order.SalesOrder', on_delete=models.SET_NULL, null=True, blank=False)
    amount = models.FloatField(default=0.0)
    amount_balance = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, default='Credit', choices=CHOICES, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order.invoice_id

#
# @receiver(post_save, sender=Transaction)
# def invoice_amount_update(sender, created, instance, **kwargs):
#     if created:
#         actual_inv_amount = instance.order.invoice_amount
#         remaining_amount = instance.order.invoice_remaining_amount
#         paid_amount = instance.amount
#         # import pdb;pdb.set_trace()
#         if paid_amount == actual_inv_amount:  # if the actual amount is same as paid amount payment is completed
#             SalesOrder.objects.filter(pk=instance.order.pk).update(invoice_status='payment_done')
#         elif paid_amount < remaining_amount:
#             balance = remaining_amount - paid_amount
#             print(f"balance:{balance},paid:{paid_amount}")
#             status = 'payment_partial'
#             rem_amount = instance.order.invoice_remaining_amount
#             # print(type(rem_amount), "rem amount")
#             if rem_amount != 0.1:
#                 rem_amount -= paid_amount
#                 if rem_amount in [0.0, 0]:
#                     status = 'payment_done'
#             elif rem_amount == 0.1:
#                 # first transaction
#                 # issue if the paid amount is bigger than balance amount it is deleted nt in first transaction
#                 rem_amount = balance
#                 if paid_amount > rem_amount:
#                     # instance.delete()
#                     print("deleted instance")
#                     SalesOrder.objects.filter(pk=instance.order.pk).update(invoice_remaining_amount=rem_amount,
#                                                                            invoice_status=status)
#                     Transaction.objects.filter(pk=instance.pk).update(amount_balance=rem_amount, status=status)
#                     raise AmountMissMatchException(f"Inital transaction of {paid_amount}")
#
#             if rem_amount < 0.0:
#                 instance.delete()
#                 print("deleted instance")
#                 raise AmountMissMatchException("Amount is Greater than balance amount !!")
#             if paid_amount > rem_amount:
#                 instance.delete()
#                 print("deleted instance")
#                 raise AmountMissMatchException("Amount is Greater than balance amount !!")
#             SalesOrder.objects.filter(pk=instance.order.pk).update(invoice_remaining_amount=rem_amount,
#                                                                    invoice_status=status)
#             Transaction.objects.filter(pk=instance.pk).update(amount_balance=rem_amount, status=status)


@receiver(post_save, sender=Transaction)
def invoice_amount_update(sender, created, instance, **kwargs):
    if created:
        actual_inv_amount = instance.order.invoice_amount
        remaining_amount = instance.order.invoice_remaining_amount
        paid_amount = instance.amount
        # import pdb;pdb.set_trace()
        if paid_amount <= 0:
            instance.delete()
            print("deleted instance")
            raise AmountMissMatchException("Enter a valid amount")
        if paid_amount > remaining_amount:
            # import pdb;pdb.set_trace()
            instance.delete()
            print("deleted instance")
            raise AmountMissMatchException("Amount is Greater than balance amount !!")
        if paid_amount == actual_inv_amount:  # if the actual amount is same as paid amount payment is completed
            SalesOrder.objects.filter(pk=instance.order.pk).update(invoice_status='payment_done')
        elif paid_amount <= remaining_amount:
            remaining_amount -= paid_amount
            print(f"remaining_amount:{remaining_amount},paid:{paid_amount}")
            status = 'payment_partial'
            # print(type(rem_amount), "rem amount")
            if remaining_amount in [0.0, 0]:
                status = 'payment_done'
                SalesOrder.objects.filter(pk=instance.order.pk).update(invoice_remaining_amount=remaining_amount,
                                                                       invoice_status=status)
                Transaction.objects.filter(pk=instance.pk).update(amount_balance=remaining_amount, status=status)
        if remaining_amount < 0.0:
            instance.delete()
            print("deleted instance")
            raise AmountMissMatchException("Amount is Greater than balance amount !!")
        # issue if the paid amount is bigger than balance amount it is deleted nt in first transaction

        SalesOrder.objects.filter(pk=instance.order.pk).update(invoice_remaining_amount=remaining_amount,
                                                               invoice_status=status)
        Transaction.objects.filter(pk=instance.pk).update(amount_balance=remaining_amount, status=status)

