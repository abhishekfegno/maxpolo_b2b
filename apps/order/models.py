from django.db import models

# Create your models here.
INVOICE_STATUS = (
    ('credit', 'CREDIT'),
    ('payment partial', 'Payment Partial'),
    ('payment done', 'Payment Done')
)



class SalesOrder(models.Model):
    order_id = models.CharField(max_length=10)
    invoice_id = models.CharField(max_length=10, null=True, blank=True)
    dealer = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_invoice = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_date = models.DateTimeField()
    invoice_date = models.DateTimeField()


    def save(self):
        if self.is_confirmed:
            self.confirmed_date = datetime.datetime.now()
        if self.is_invoice:
            self.invoice_date = datetime.dateime.now()

    def __str__(self):
        return self.order_id


class SalesOrderLine(models.Model):
    order = models.ForeignKey('order.SalesOrder', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('catalogue.Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

