from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models
# Create your models here.
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

INVOICE_STATUS = (
    ('new', 'New'),
    ('credit', 'Credit'),
    ('payment_partial', 'Payment Partial'),
    ('payment_done', 'Payment Done')
)


class SalesOrder(models.Model):
    order_id = models.CharField(max_length=10)
    invoice_id = models.CharField(max_length=10, null=True, blank=True)
    dealer = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=False)

    is_quotation = models.BooleanField(default=True)
    is_cancelled = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_invoice = models.BooleanField(default=False)

    invoice_status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='new')
    invoice_amount = models.FloatField(default=0.0)
    invoice_remaining_amount = models.FloatField(default=0.1)  # must be set to 0.1 for programming purpose

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    confirmed_date = models.DateTimeField(null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.invoice_id:
            return self.invoice_id
        return self.order_id

    @property
    def order_type(self):
        if self.is_confirmed:
            order = 'salesorder'
        elif self.is_invoice:
            order = 'invoice'
        else:
            order = 'quotation'
        return order

    @property
    def has_transaction(self):
        if self.transaction_set.all():
            return True
        return False

    @property
    def id_as_text(self):
        return f'ORD{str(self.pk).zfill(6)}'

    @property
    def total_line_quantity(self):
        return self.line.all().aggregate(total_quantity=Sum('quantity')).values()

    def save(self, **kwargs):
        if self.is_confirmed and self.is_cancelled:
            self.is_cancelled = False
        super(SalesOrder, self).save(**kwargs)


class SalesOrderLine(models.Model):
    order = models.ForeignKey('order.SalesOrder', on_delete=models.SET_NULL, related_name='line', null=True, blank=True)
    product = models.ForeignKey('catalogue.Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator])

    def __str__(self):
        return self.product.name


@receiver(post_save, sender=SalesOrder)
def create_order_ids(sender, instance, created, **kwargs):
    if created:
        SalesOrder.objects.filter(pk=instance.pk).update(order_id='QN' + f'{instance.pk}'.zfill(6))
    if instance.is_confirmed:
        print("changing order_id")
        SalesOrder.objects.filter(pk=instance.pk).update(confirmed_date=datetime.now(), is_quotation=False,
                                                         order_id='SO' + f'{instance.pk}'.zfill(6))
    if instance.is_invoice and instance.is_confirmed:
        print("changing invoice_id")
        SalesOrder.objects.filter(pk=instance.pk).update(invoice_date=datetime.now(), is_confirmed=False,
                                                         invoice_id='INV' + f'{instance.pk}'.zfill(6))
    # if instance.invoice_amount:
    #     print("credit status")
    #     SalesOrder.objects.filter(pk=instance.pk).update(invoice_status='credit')
    return instance
