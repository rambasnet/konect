# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 11:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_key', models.CharField(max_length=128)),
                ('key_expires', models.DateTimeField(null=True)),
                ('local', models.CharField(max_length=10, null=True)),
                ('profile_picture', models.CharField(max_length=256, null=True)),
                ('current_title', models.CharField(max_length=100, null=True)),
                ('public_email', models.CharField(max_length=256, null=True)),
                ('banner_picture', models.CharField(max_length=256, null=True)),
                ('tagline', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=30, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
