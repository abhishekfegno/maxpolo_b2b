from django.db import models
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


class Product(models.Model):
    name = models.CharField(max_length=50)
    product_code = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


