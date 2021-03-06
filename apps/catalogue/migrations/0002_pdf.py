# Generated by Django 4.0.5 on 2022-06-13 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='pdf/product/')),
                ('is_public', models.BooleanField(default=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                               to='catalogue.category')),
            ],
        ),
    ]
