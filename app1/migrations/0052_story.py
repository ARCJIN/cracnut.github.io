# Generated by Django 4.0.3 on 2022-03-26 04:22

import app1.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0051_post_club_post_is_private'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=500)),
                ('profile_image', models.ImageField(blank=True, default=app1.models.get_default_profile_image, null=True, upload_to='postprofileimages/')),
                ('is_block', models.BooleanField(default=False, null=True)),
                ('is_special', models.BooleanField(default=False, null=True)),
                ('is_promoted', models.BooleanField(default=False, null=True)),
                ('is_highdemand', models.BooleanField(default=False, null=True)),
                ('is_closed_friend', models.BooleanField(default=False, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('composer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.customer')),
                ('likers', models.ManyToManyField(related_name='storys_liked', to='app1.customer')),
            ],
        ),
    ]
