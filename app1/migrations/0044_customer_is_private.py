# Generated by Django 3.2.7 on 2022-03-20 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0043_post_num_of_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_private',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
