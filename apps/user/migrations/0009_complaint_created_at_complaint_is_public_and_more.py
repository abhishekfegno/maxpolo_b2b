# Generated by Django 4.0.5 on 2022-06-28 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_banners_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='complaint',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='complaint',
            name='ticket_id',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='complaint',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='banners',
            name='photo',
            field=models.ImageField(blank=True, default='default/banner.jpg', null=True, upload_to='banners/'),
        ),
    ]
