# Generated by Django 3.1.3 on 2022-06-29 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20220629_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='ticket_id',
        ),
    ]