# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 00:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('eprofile', '0012_auto_20160109_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 9, 0, 29, 45, 767566, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
    ]
