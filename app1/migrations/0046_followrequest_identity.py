# Generated by Django 3.2.7 on 2022-03-23 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0045_auto_20220323_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='followrequest',
            name='identity',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
