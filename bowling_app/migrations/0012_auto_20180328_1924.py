# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-29 00:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowling_app', '0011_auto_20180328_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='current_frame_id',
            field=models.IntegerField(default=1),
        ),
    ]
