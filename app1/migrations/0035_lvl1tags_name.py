# Generated by Django 3.2.7 on 2022-01-09 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0034_lvl3tags_lvl4tags_lvl5tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='lvl1tags',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]