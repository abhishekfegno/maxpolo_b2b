# Generated by Django 4.0.5 on 2022-06-09 09:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='dealer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
