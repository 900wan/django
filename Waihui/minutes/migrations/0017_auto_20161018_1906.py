# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minutes', '0016_auto_20161018_1844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='attended_entrie',
        ),
        migrations.AddField(
            model_name='profile',
            name='entry',
            field=models.ManyToManyField(related_name='attendees_nouser', to='minutes.Entry', verbose_name='\u51fa\u5e2d\u7684\u4f1a\u8bae'),
        ),
    ]
