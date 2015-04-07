# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0006_auto_20150330_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='menu_item_category',
        ),
        migrations.DeleteModel(
            name='MenuItemCategory',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='type',
            field=models.CharField(default='', max_length=32, choices=[(b'APPETIZER', b'APPETIZER'), (b'MAIN', b'MAIN'), (b'DESSERT', b'DESSERT'), (b'BEVERAGE', b'BEVERAGE')]),
            preserve_default=False,
        ),
    ]
