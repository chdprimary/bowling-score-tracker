# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-28 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowling_app', '0002_roll_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roll',
            name='score',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
