from django.db import models


# Create your models here.


class Branch(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=30)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
