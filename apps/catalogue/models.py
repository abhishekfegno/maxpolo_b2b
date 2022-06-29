import os

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.fields import AutoSlugField
from treebeard.mp_tree import MP_Node


# Create your models here.
from apps.user.models import Dealer
from lib.sent_email import EmailHandler


class Brand(models.Model):
    name = models.CharField(max_length=20, unique=True)

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
        return f"{self.name}"


class PDF(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    slug = AutoSlugField(max_length=50, populate_from='title', null=True, blank=True)
    image = models.ImageField(upload_to='pdf/product/', blank=True, null=True)
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
    image = models.ImageField(upload_to='product/', default='default/image_not_found.jpg', null=True, blank=True)
    product_code = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def photo_url(self):
        if self.image:
            return self.image.url
        return settings.MEDIA_URL + settings.DEFAULT_IMAGE


@receiver(post_save, sender=PDF)
def sent_email_pdf(sender, created, instance, **kwargs):
    recipients = [i for i in Dealer.objects.all().values('email', 'first_name')]
    if created:
        EmailHandler().sent_mail_for_banners(recipients, instance)
