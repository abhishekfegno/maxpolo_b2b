# Generated by Django 4.0.5 on 2022-07-04 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_alter_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('credit', 'Credit'), ('payment_partial', 'Payment Partial'), ('payment_done', 'Payment Done'), ('cancelled', 'Cancelled')], default='Credit', max_length=20, null=True),
        ),
    ]