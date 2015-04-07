# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='is_email_verified',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='mobile_number',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='phone_number',
        ),
    ]
