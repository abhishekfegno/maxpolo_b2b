# Generated by Django 4.0.5 on 2022-06-20 10:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payment', '0002_transaction_amount_balance_transaction_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(default='Credit', max_length=20, null=True),
        ),
    ]
