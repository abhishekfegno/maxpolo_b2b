# Generated by Django 3.1.3 on 2022-06-29 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('executivetracking', '0004_alter_checkpoint_id_alter_crashreport_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkpoint',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='crashreport',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='zone',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
