# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import foodie.models_mixins
import django.utils.timezone
from django.conf import settings
import foodie.storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.CharField(unique=True, max_length=64, verbose_name=b'email')),
                ('first_name', models.CharField(max_length=32, null=True, verbose_name=b'first name', blank=True)),
                ('last_name', models.CharField(max_length=32, null=True, verbose_name=b'last name', blank=True)),
                ('image', models.ImageField(storage=foodie.storage.OverwriteStorage(), upload_to=b'base_user/images', null=True, verbose_name=b'image', blank=True)),
                ('thumbnail', models.ImageField(storage=foodie.storage.OverwriteStorage(), upload_to=b'base_user/thumbnails', null=True, verbose_name=b'thumbnail', blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name=b'date joined')),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=256, null=True, blank=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('mobile_number', models.CharField(max_length=32, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=32, null=True, blank=True)),
                ('base_user', models.OneToOneField(related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(foodie.models_mixins.BaseUserMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Dispatcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=64, verbose_name=b'email')),
                ('first_name', models.CharField(max_length=32, null=True, verbose_name=b'first name', blank=True)),
                ('last_name', models.CharField(max_length=32, null=True, verbose_name=b'last name', blank=True)),
                ('image', models.ImageField(storage=foodie.storage.OverwriteStorage(), upload_to=b'dispatcher/images', null=True, verbose_name=b'image', blank=True)),
                ('thumbnail', models.ImageField(storage=foodie.storage.OverwriteStorage(), upload_to=b'dispatcher/thumbnails', null=True, verbose_name=b'thumbnail', blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(storage=foodie.storage.OverwriteStorage(), upload_to=b'menu_items/images', null=True, verbose_name=b'image', blank=True)),
                ('thumbnail', models.ImageField(storage=foodie.storage.OverwriteStorage(), upload_to=b'menu_items/thumbnails', null=True, verbose_name=b'thumbnail', blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItemCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('image', models.ImageField(storage=foodie.storage.OverwriteStorage(), upload_to=b'menu_items/images', null=True, verbose_name=b'image', blank=True)),
                ('thumbnail', models.ImageField(storage=foodie.storage.OverwriteStorage(), upload_to=b'menu_items/thumbnails', null=True, verbose_name=b'thumbnail', blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_user', models.OneToOneField(related_name='operator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(foodie.models_mixins.BaseUserMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=32, choices=[(b'RECEIVED', b'RECEIVED'), (b'CANCELLED', b'CANCELLED'), (b'DELIVERED', b'DELIVERED')])),
                ('delivery_time_from', models.DateTimeField()),
                ('delivery_time_to', models.DateTimeField()),
                ('customer', models.ForeignKey(related_name='order', to='foodie.Customer')),
                ('dispatcher', models.ForeignKey(related_name='order', to='foodie.Dispatcher')),
                ('menu_items', models.ManyToManyField(related_name='order', to='foodie.MenuItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServiceRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField()),
                ('taste', models.BooleanField(default=True)),
                ('delivery', models.BooleanField(default=True)),
                ('packaging', models.BooleanField(default=True)),
                ('support', models.BooleanField(default=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('customer', models.ForeignKey(related_name='service_rating', to='foodie.Customer')),
                ('order', models.ForeignKey(related_name='service_rating', to='foodie.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='menu_item_category',
            field=models.ForeignKey(related_name='menu_items', to='foodie.MenuItemCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menu',
            name='menu_items',
            field=models.ManyToManyField(to='foodie.MenuItem'),
            preserve_default=True,
        ),
    ]
