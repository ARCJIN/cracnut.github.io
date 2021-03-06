# Generated by Django 3.2.7 on 2022-01-07 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0030_transfer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units', models.PositiveIntegerField(default=0, null=True)),
                ('keeper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='keeper', to='app1.seller')),
                ('payer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payer', to='app1.customer')),
            ],
        ),
    ]
