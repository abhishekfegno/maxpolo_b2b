# Generated by Django 4.0.5 on 2022-06-15 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('catalogue', '0002_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pdf',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
