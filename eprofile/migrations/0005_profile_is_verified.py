# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-07 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eprofile', '0004_auto_20160107_0723'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.NullBooleanField(),
        ),
    ]