# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-28 22:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowling_app', '0005_roll_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='running_total_score',
            field=models.IntegerField(default=0),
        ),
    ]
