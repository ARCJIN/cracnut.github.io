# Generated by Django 3.2.7 on 2021-12-27 08:53

import app1.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_customer_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_image',
            field=models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to=''),
        ),
    ]
