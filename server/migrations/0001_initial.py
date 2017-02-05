# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-20 19:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Boardgames',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('img', models.CharField(max_length=1000)),
                ('thumbnail', models.CharField(max_length=1000)),
                ('bggid', models.IntegerField(db_column='bggId', default=0, unique=True)),
                ('minage', models.IntegerField(default=0)),
                ('playingtime', models.IntegerField(default=0)),
                ('minplayers', models.IntegerField(default=0)),
                ('maxplayers', models.IntegerField(default=0)),
                ('yearpublished', models.IntegerField(default=0)),
                ('maxplaytime', models.IntegerField(default=0)),
                ('minplaytime', models.IntegerField(default=0)),
                ('average', models.FloatField(default=0)),
                ('usersrated', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boardgame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Boardgames')),
            ],
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('duration', models.IntegerField(default=0)),
                ('boardgame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Boardgames')),
            ],
        ),
        migrations.CreateModel(
            name='Plays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Matches')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100, unique=True)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('img', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='plays',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Users'),
        ),
        migrations.AddField(
            model_name='friends',
            name='user1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user1', to='server.Users'),
        ),
        migrations.AddField(
            model_name='friends',
            name='user2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user2', to='server.Users'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.Users'),
        ),
    ]
