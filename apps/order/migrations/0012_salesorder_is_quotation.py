# Generated by Django 4.0.5 on 2022-06-20 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_alter_salesorder_invoice_remaining_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='is_quotation',
            field=models.BooleanField(default=True),
        ),
    ]
