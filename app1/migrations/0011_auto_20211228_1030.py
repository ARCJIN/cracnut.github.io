# Generated by Django 3.2.7 on 2021-12-28 05:00

import app1.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_auto_20211228_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_image',
            field=models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='profile_image',
            field=models.ImageField(blank=True, default=app1.models.get_default_profile_image, null=True, upload_to=''),
        ),
    ]
