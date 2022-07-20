# Generated by Django 4.0.5 on 2022-07-12 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_auto_20220704_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesorder',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='invoice_remaining_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='salesorderline',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]