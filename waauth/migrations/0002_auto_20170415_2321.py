# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-16 04:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wauser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wa_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
