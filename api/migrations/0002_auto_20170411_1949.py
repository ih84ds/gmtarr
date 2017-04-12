# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 00:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='rating',
        ),
        migrations.AddField(
            model_name='flight',
            name='ntrp',
            field=models.CharField(blank=True, max_length=31, null=True),
        ),
        migrations.AddField(
            model_name='flight',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='phone',
            field=models.CharField(blank=True, max_length=31, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='users',
            field=models.ManyToManyField(related_name='players', to=settings.AUTH_USER_MODEL),
        ),
    ]
