# Generated by Django 4.0.5 on 2022-06-16 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('executivetracking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkpoint',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='crashreport',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='zone',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]