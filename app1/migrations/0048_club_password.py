# Generated by Django 3.2.7 on 2022-03-23 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0047_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='password',
            field=models.CharField(blank=True, default='0000', max_length=200, null=True),
        ),
    ]
