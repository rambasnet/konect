# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-07 05:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eprofile', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='card_address1',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='card_address2',
            field=models.CharField(max_length=256, null=True),
        ),
    ]