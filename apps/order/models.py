from django.db import models

# Create your models here.


class PurchaseOrder(models.Model):
    order_id = models.CharField(max_length=10)
    dealer = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.order_id


class SalesOrder(models.Model):
    order_id = models.CharField(max_length=10)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.order_id


class SalesOrderLine(models.Model):
    order = models.ForeignKey('order.SalesOrder', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('catalogue.Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

