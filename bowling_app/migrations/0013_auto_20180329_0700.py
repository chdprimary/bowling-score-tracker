# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-29 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowling_app', '0012_auto_20180328_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='start_frame_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='frame',
            name='frame_score',
            field=models.IntegerField(default=-1),
        ),
    ]
