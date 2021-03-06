# Generated by Django 3.2.7 on 2021-12-27 06:58

import app1.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=50, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='created_date')),
                ('address', models.CharField(max_length=200, null=True)),
                ('crypto_owned', models.FloatField(null=True)),
                ('profile_image', models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to=app1.models.get_customer_profile_image_filepath)),
                ('money_owned', models.FloatField(null=True)),
                ('is_certified', models.BooleanField(default=False, null=True)),
                ('is_block', models.BooleanField(default=False, null=True)),
                ('is_login', models.BooleanField(default=False, null=True)),
                ('is_admin', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=50, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='created_date')),
                ('home_address', models.CharField(max_length=200, null=True)),
                ('shop_address', models.CharField(max_length=200, null=True)),
                ('crypto_owned', models.FloatField(null=True)),
                ('profile_image', models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to=app1.models.get_customer_profile_image_filepath)),
                ('money_owned', models.FloatField(null=True)),
                ('is_certified', models.BooleanField(default=False, null=True)),
                ('is_block', models.BooleanField(default=False, null=True)),
                ('is_login', models.BooleanField(default=False, null=True)),
                ('is_admin', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('itemid', models.CharField(default=0, max_length=50)),
                ('category', models.CharField(blank=True, choices=[('tshirt', 'tshirt'), ('shirt', 'shirt'), ('hoodie', 'hoodie'), ('cup', 'cup'), ('phone covers', 'phone covers'), ('bands', 'bands'), ('gym vests', 'gym vests'), ('keychain', 'keychain'), ('posters', 'posters'), ('stickers', 'stickers'), ('notebooks', 'notebooks'), ('caps', 'caps'), ('bags', 'bags'), ('socks', 'socks'), ('footwear', 'footwear'), ('masks', 'masks')], max_length=20)),
                ('colour', models.CharField(blank=True, choices=[('red', 'red'), ('blue', 'blue'), ('green', 'green'), ('orange', 'orange'), ('purple', 'purple'), ('yellow', 'yellow'), ('black', 'black'), ('white', 'white')], max_length=20)),
                ('material', models.CharField(blank=True, max_length=20)),
                ('size', models.CharField(blank=True, choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')], max_length=5)),
                ('desc', models.CharField(blank=True, max_length=500, null=True)),
                ('number_of_likes', models.IntegerField(default=0)),
                ('number_of_views', models.IntegerField(default=0)),
                ('number_of_purchases', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_block', models.BooleanField(default=False, null=True)),
                ('fashion_of_the_week', models.BooleanField(default=False, null=True)),
                ('is_special', models.BooleanField(default=False, null=True)),
                ('is_promoted', models.BooleanField(default=False, null=True)),
                ('is_highdemand', models.BooleanField(default=False, null=True)),
                ('profile_image1', models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to=app1.models.get_product_profile_image_filepath)),
                ('profile_image2', models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to=app1.models.get_product_profile_image_filepath)),
                ('profile_image3', models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to=app1.models.get_product_profile_image_filepath)),
                ('profile_image4', models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to=app1.models.get_product_profile_image_filepath)),
                ('profile_image5', models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to=app1.models.get_product_profile_image_filepath)),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.customer')),
                ('tags', models.ManyToManyField(to='app1.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=500)),
                ('profile_image', models.ImageField(blank=True, default=app1.models.get_default_profile_image, max_length=255, null=True, upload_to='post_profile_images')),
                ('is_block', models.BooleanField(default=False, null=True)),
                ('is_special', models.BooleanField(default=False, null=True)),
                ('is_promoted', models.BooleanField(default=False, null=True)),
                ('is_highdemand', models.BooleanField(default=False, null=True)),
                ('number_of_likes', models.IntegerField(default=0)),
                ('number_of_comments', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(choices=[('Transaction Failed', 'Transaction Failed'), ('Transaction to be verfied', 'Transaction to be verified'), ('Order Confirmed', 'Order Confirmed'), ('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Refund Request Active', 'Refund Request Active'), ('Refund Successful', 'Refund Successful')], max_length=30, null=True)),
                ('is_block', models.BooleanField(default=False, null=True)),
                ('mode_of_payment', models.CharField(choices=[('CASH', 'CASH'), ('CC', 'CC'), ('Debit Card', 'Debit Card'), ('GooglePay', 'GooglePay')], max_length=30, null=True)),
                ('is_transaction_successfull', models.BooleanField(default=False, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.customer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.product')),
            ],
        ),
    ]
