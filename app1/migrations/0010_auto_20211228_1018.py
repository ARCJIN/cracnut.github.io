# Generated by Django 3.2.7 on 2021-12-28 04:48

import app1.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_auto_20211228_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_image',
            field=models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='seller',
            name='profile_image',
            field=models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to=''),
        ),
    ]