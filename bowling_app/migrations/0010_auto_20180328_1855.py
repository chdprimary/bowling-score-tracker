# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-28 23:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bowling_app', '0009_game_current_frame'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='current_frame',
            new_name='current_frame_id',
        ),
    ]