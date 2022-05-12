from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    genre = models.CharField(max_length=50, primary_key=True)


class Game(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    img_src = models.CharField(max_length=150)
    developer = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    release = models.DateTimeField('Release Date')


class Character(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=50)


class LevelUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    birthday = models.CharField(max_length=50)
    img_src = models.CharField(max_length=150)
    location = models.CharField(max_length=50)
    joined = models.DateTimeField('Joined')
    bio = models.CharField(max_length=500)
    favorite_genres = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)


class UserStats(models.Model):
    user = models.OneToOneField(LevelUser, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    playing = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)
    on_hold = models.IntegerField(default=0)
    dropped = models.IntegerField(default=0)
    plan_to_play = models.IntegerField(default=0)
    games = models.ForeignKey(Game, on_delete=models.CASCADE)
    characters = models.ForeignKey(Character, on_delete=models.CASCADE)


class Review(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    comment = models.CharField(max_length=500)
