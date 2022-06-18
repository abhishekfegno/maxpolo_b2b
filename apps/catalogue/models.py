import os

from django.db import models
from django_extensions.db.fields import AutoSlugField
from treebeard.mp_tree import MP_Node

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Category(MP_Node):

    """
     To add Root: Category.add_root(name='Computer Hardware')
     To add Child: Category.objects.get(name='Computer Hardware').add_child(name='Memory')
     To add Sibling: Category.objects.get(name='Memory').add_sibling(name='Desktop Memory')
    """
    name = models.CharField(max_length=20)
    node_order_by = ['name']

    def __str__(self):
        return 'Category: {}'.format(self.name)


class PDF(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    slug = AutoSlugField(max_length=50, populate_from='title', null=True, blank=True)
    file = models.FileField(upload_to='pdf/product/', blank=True, null=True)
    is_public = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='pdf', blank=False, null=True)

    def __str__(self):
        return self.category.name

    def filename(self): return os.path.basename(self.file.name)

    def save(self, *args, **kwargs):
        self.slug = str(self.title).lower().replace(' ', '-')
        return super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    product_code = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


