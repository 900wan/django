# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 10:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minutes', '0014_auto_20161018_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='attended_entrie',
            field=models.ManyToManyField(to='minutes.Entry'),
        ),
    ]