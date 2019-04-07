# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-07 04:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20170421_0938'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flight',
            options={'ordering': ['-year', 'name', 'id']},
        ),
        migrations.AlterModelOptions(
            name='league',
            options={'ordering': ['-year', 'name', 'id']},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['scheduled_date', 'id']},
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['name', 'id']},
        ),
    ]
