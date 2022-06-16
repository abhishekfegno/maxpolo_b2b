from datetime import datetime

from django.db import models

# Create your models here.
INVOICE_STATUS = (
    ('new', 'NEW'),
    ('credit', 'CREDIT'),
    ('payment partial', 'Payment Partial'),
    ('payment done', 'Payment Done')
)


class SalesOrder(models.Model):
    order_id = models.CharField(max_length=10)
    invoice_id = models.CharField(max_length=10, null=True, blank=True)
    dealer = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=False)
    is_cancelled = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_invoice = models.BooleanField(default=False)
    invoice_status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='new')
    invoice_amount = models.FloatField(default=0.0)
    invoice_remaining_amount = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    confirmed_date = models.DateTimeField(null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_confirmed:
            self.confirmed_date = datetime.now()
        if self.is_invoice:
            self.invoice_date = datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id

    @property
    def id_as_text(self):
        return 'ORD' + f'{self.pk}'.zfill(6)


class SalesOrderLine(models.Model):
    order = models.ForeignKey('order.SalesOrder', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('catalogue.Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

