# Generated by Django 4.0.3 on 2022-05-25 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0056_bagitem_delete_bag'),
    ]

    operations = [
        migrations.AddField(
            model_name='bagitem',
            name='item_in_bag',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
