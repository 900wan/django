# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 10:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minutes', '0013_auto_20161018_1746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='attended_entries',
            new_name='attended_entrie',
        ),
    ]