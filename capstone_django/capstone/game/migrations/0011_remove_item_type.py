# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 21:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20170811_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='type',
        ),
    ]
