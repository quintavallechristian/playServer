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
    #id = models.AutoField(db_column='boardgame_Id', primary_key=True, null=False)  # Field name made lowercase.
    title = models.CharField(max_length=100)
    description = models.TextField()
    img = models.CharField(max_length=1000)
    thumbnail = models.CharField(max_length=1000)
    bggid = models.IntegerField(db_column='bggId', unique=True, default=0)  # Field name made lowercase.
    minage=models.IntegerField(default=0)
    playingtime=models.IntegerField(default=0)
    minplayers=models.IntegerField(default=0)
    maxplayers=models.IntegerField(default=0)
    yearpublished=models.IntegerField(default=0)
    maxplaytime=models.IntegerField(default=0)
    minplaytime=models.IntegerField(default=0)
    average=models.FloatField(default=0)
    usersrated=models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id) +" - "+self.title

class Users(models.Model):
    #user_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=100)
    username = models.CharField(unique=True, max_length=25)
    password = models.CharField(max_length=256)
    img = models.CharField(max_length=256)

    def __unicode__(self):
        return self.username

class Matches(models.Model):
    #match_id = models.AutoField(primary_key=True)
    boardgame = models.ForeignKey(Boardgames, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=256)
    time = models.DateTimeField()
    location = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)

    def __unicode__(self):
        return "Match " + str(self.id) + " - game: " + str(self.boardgame).decode('utf8')

class Friends(models.Model) :
    user1 = models.ForeignKey(Users, related_name='user1', on_delete=models.CASCADE, null=True)
    user2 = models.ForeignKey(Users, related_name='user2', on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return "User id 1: "+str(self.user1) + " and User id 2: " + str(self.user2)

class Favourites(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    boardgame = models.ForeignKey(Boardgames, on_delete=models.CASCADE)

    def __unicode__(self):
        return "Game id "+str(self.boardgame).decode('utf8') + " and User id " + str(self.user)

class Plays(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    match = models.ForeignKey(Matches, on_delete=models.CASCADE)
    points = models.IntegerField(default=999999)

    def __unicode__(self):
        return str(self.match).decode('utf8') + " and User id " + str(self.user)

class Dictionary(models.Model):
    word = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default="", blank=True)

    def __unicode__(self):
        return str(self.word).decode('utf8') + ": " + str(self.description)

class Templates(models.Model):
    boardgame = models.ForeignKey(Boardgames, on_delete=models.CASCADE)
    word = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    bonus = models.IntegerField(default=1)

    def __unicode__(self):
        return str(self.word).decode('utf8') + ": " + str(self.boardgame)

class DetailedPoints(models.Model):
    template = models.ForeignKey(Templates, on_delete=models.CASCADE)
    play = models.ForeignKey(Plays, on_delete=models.CASCADE)
    detailed_points = models.IntegerField(default=999999)
    notes = models.CharField(max_length=100, default="", blank=True)

    def __unicode__(self):
        return str(self.template).decode('utf8') + ": " + str(self.play)