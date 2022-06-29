# Generated by Django 4.0.5 on 2022-06-24 06:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('catalogue', '0010_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='public/default/image_not_found.jpg', null=True,
                                    upload_to='product/'),
        ),
    ]
