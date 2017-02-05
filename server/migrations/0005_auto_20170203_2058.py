# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-03 19:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_matches_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailedPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailed_points', models.IntegerField(default=999999)),
                ('notes', models.CharField(default='', max_length=100)),
                ('play', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Plays')),
            ],
        ),
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Templates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='boardgames',
            name='maxplayers',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='boardgames',
            name='minage',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='boardgames',
            name='minplayers',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='boardgames',
            name='usersrated',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='boardgames',
            name='yearpublished',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='templates',
            name='boardgame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Boardgames'),
        ),
        migrations.AddField(
            model_name='templates',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Dictionary'),
        ),
        migrations.AddField(
            model_name='detailedpoints',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Templates'),
        ),
    ]