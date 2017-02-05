# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Boardgames(models.Model):
    boardgame_id = models.AutoField(db_column='boardgame_Id', primary_key=True)  # Field name made lowercase.
    boardgame_title = models.CharField(max_length=100)
    boardgame_description = models.TextField()
    boardgame_img = models.CharField(max_length=256)
    boardgame_bggvote = models.FloatField(db_column='boardgame_bggVote')  # Field name made lowercase.
    boardgame_bggid = models.IntegerField(db_column='boardgame_bggId', unique=True)  # Field name made lowercase.
    boardgame_family = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'boardgames'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Matches(models.Model):
    match_id = models.AutoField(primary_key=True)
    match_gamesid = models.IntegerField(db_column='match_gamesId')  # Field name made lowercase.
    match_time = models.DateTimeField()
    match_location = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'matches'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.CharField(unique=True, max_length=100)
    user_username = models.CharField(unique=True, max_length=20)
    user_password = models.CharField(max_length=256)
    user_img = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'users'
