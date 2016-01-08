# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 18:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locale', models.CharField(max_length=10, null=True)),
                ('profile_photo', models.CharField(max_length=256, null=True)),
                ('cover_photo', models.CharField(max_length=256, null=True)),
                ('card_name', models.CharField(max_length=100, null=True)),
                ('card_title', models.CharField(max_length=100, null=True)),
                ('card_department', models.CharField(max_length=100, null=True)),
                ('card_employer', models.CharField(max_length=100, null=True)),
                ('card_email', models.EmailField(max_length=254, null=True)),
                ('card_phone', models.CharField(max_length=30)),
                ('card_office', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]