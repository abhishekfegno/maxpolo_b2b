# Generated by Django 4.0.5 on 2022-07-12 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_alter_salesorder_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='cancelled_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
