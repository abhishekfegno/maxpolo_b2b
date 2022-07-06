from datetime import datetime

from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models
# Create your models here.
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property

from apps.notification.events import NotificationEvent
from lib.sent_email import EmailHandler

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
    invoice_remaining_amount = models.FloatField(default=0)
    invoice_pdf = models.FileField(upload_to='invoice/', validators=[FileExtensionValidator(['pdf'])], blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    confirmed_date = models.DateTimeField(null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)
    __show_dealer_in_str__ = False

    class Meta:
        unique_together = ('order_id', 'invoice_id')

    @property
    def percentage_paid(self):
        return ((self.invoice_amount - self.invoice_remaining_amount) * 10000 // self.invoice_amount)/100

    def __str__(self):
        if self.invoice_id:
            # if self.__show_dealer_in_str__:
            return f"{self.invoice_id} - {self.dealer.get_full_name()}"
            # return self.invoice_id
        return self.order_id

    QUOTATION = "quotation"
    INVOICED = "invoice"
    CONFIRMED = "salesorder"
    CANCELLED = "cancelled"

    @property
    def status(self):
        if self.is_invoice:
            return self.INVOICED
        elif self.is_confirmed:
            return self.CONFIRMED
        elif self.is_cancelled:
            return self.CANCELLED
        return self.QUOTATION

    @status.setter
    def status(self, value):
        if value == self.QUOTATION:
            spread = 0, 0, 0, 1
        elif value == self.CANCELLED:
            spread = 0, 0, 1, 0
        elif value == self.CONFIRMED:
            spread = 0, 1, 0, 0
        elif value == self.INVOICED:
            spread = 1, 0, 0, 0
        else:
            return
        self.is_invoice, self.is_confirmed, self.is_cancelled, self.is_quotation = spread

    @property
    def order_type(self):
        return self.status

    @cached_property
    def has_transaction(self):
        return self.transaction_set.exists()

    @property
    def id_as_text(self):
        return f'ORD{str(self.pk).zfill(6)}'

    @property
    def total_line_quantity(self):
        return self.line.all().aggregate(total_quantity=Sum('quantity')).values()

    def recalculate_remaining(self):
        net_paid_amount = self.transaction_set.all().exclude(status='cancelled').aggeregate(sum=Sum('amount'))['sum'] or 0
        self.invoice_remaining_amount = max(self.invoice_amount - float(net_paid_amount), 0)
        if self.invoice_remaining_amount == self.invoice_amount:
            self.status = 'credit'
        elif self.invoice_remaining_amount == 0:
            self.status = 'payment_done'
        else:
            self.status = 'payment_partial'
        self.save()

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
        message = f"Dear {instance.dealer}!! Your order {instance.id_as_text} has been placed"
        EmailHandler().event_for_orders(instance)
        NotificationEvent().event_for_orders(instance, message)
        SalesOrder.objects.filter(pk=instance.pk).update(order_id='QN' + f'{instance.pk}'.zfill(6))
    if instance.is_confirmed:
        print("changing order_id")
        message = f"Dear {instance.dealer}!! Your order {instance.id_as_text} has been  has been confirmed"
        EmailHandler().event_for_orders(instance)
        NotificationEvent().event_for_orders(instance, message)
        SalesOrder.objects.filter(pk=instance.pk).update(is_quotation=False)
    if instance.is_invoice and instance.is_confirmed:
        print("changing invoice_id")
        message = f"Dear {instance.dealer}!! Your order {instance.id_as_text} has been invoiced"
        EmailHandler().event_for_orders(instance)
        NotificationEvent().event_for_orders(instance, message)
        SalesOrder.objects.filter(pk=instance.pk).update(is_confirmed=False,
                                                         invoice_remaining_amount=instance.invoice_amount)
    # if instance.invoice_amount:
    #     print("credit status")
    #     SalesOrder.objects.filter(pk=instance.pk).update(invoice_status='credit')
    return instance
