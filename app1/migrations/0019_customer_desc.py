# Generated by Django 3.2.7 on 2021-12-28 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0018_auto_20211228_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='desc',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
