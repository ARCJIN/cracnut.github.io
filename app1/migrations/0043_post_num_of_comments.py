# Generated by Django 3.2.7 on 2022-03-18 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0042_auto_20220215_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='num_of_comments',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
