# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 02:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=63)),
                ('year', models.IntegerField(db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(db_index=True)),
                ('status', models.CharField(blank=True, max_length=63, null=True)),
                ('score', models.CharField(blank=True, max_length=63, null=True)),
                ('winner', models.IntegerField(blank=True, choices=[(1, 'home'), (2, 'visitor'), (3, 'double default')], null=True)),
                ('scheduled_date', models.DateField(blank=True, null=True)),
                ('played_date', models.DateField(blank=True, null=True)),
                ('entry_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='api.Flight')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=63)),
                ('gender', models.IntegerField(blank=True, choices=[(1, 'male'), (2, 'female')], null=True)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('flights', models.ManyToManyField(related_name='players', to='api.Flight')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='home_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_matches', to='api.Player'),
        ),
        migrations.AddField(
            model_name='match',
            name='visitor_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitor_matches', to='api.Player'),
        ),
    ]
