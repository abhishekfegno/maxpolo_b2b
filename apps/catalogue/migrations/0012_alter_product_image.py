# Generated by Django 4.0.5 on 2022-06-28 04:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('catalogue', '0011_alter_brand_name_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='default/image_not_found.jpg', null=True, upload_to='product/'),
        ),
    ]