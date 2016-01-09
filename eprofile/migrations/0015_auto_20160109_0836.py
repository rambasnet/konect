# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 08:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eprofile', '0014_auto_20160109_0345'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(editable=False)),
                ('company', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=256, null=True)),
                ('title', models.CharField(max_length=100)),
                ('month_from', models.IntegerField(blank=True, null=True)),
                ('year_from', models.IntegerField(blank=True, null=True)),
                ('month_to', models.IntegerField(blank=True, null=True)),
                ('year_to', models.IntegerField(blank=True, null=True)),
                ('current', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eprofile.Profile')),
            ],
            options={
                'ordering': ['-year_to', '-month_to'],
            },
        ),
        migrations.RenameField(
            model_name='education',
            old_name='address',
            new_name='location',
        ),
        migrations.AddField(
            model_name='education',
            name='current',
            field=models.BooleanField(default=False),
        ),
    ]
