# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-07 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eprofile', '0003_auto_20160107_0536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='card_email',
            field=models.EmailField(max_length=256, null=True),
        ),
    ]