# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-13 15:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0002_freeproxy_date_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freeproxy',
            name='date_time',
        ),
    ]
