# Generated by Django 3.1.3 on 2022-07-04 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0007_alter_branch_id_alter_warehouse_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]