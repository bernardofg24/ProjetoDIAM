from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    genre = models.CharField(max_length=50, primary_key=True)


class Game(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='games/')
    developer = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    release = models.DateTimeField('Release Date')


class Character(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=50)


class LevelUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50, default="Prefer not")
    birthday = models.CharField(max_length=50)
    img_src = models.CharField(max_length=150)
    location = models.CharField(max_length=50, default="Earth")
    joined = models.DateTimeField('Joined')
    bio = models.CharField(max_length=500, default="Your Bio!")
    favorite_genres = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user


class UserStats(models.Model):
    leveluser = models.OneToOneField(LevelUser, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    playing = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)
    on_hold = models.IntegerField(default=0)
    dropped = models.IntegerField(default=0)
    plan_to_play = models.IntegerField(default=0)
    games = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    characters = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)


class Review(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    comment = models.CharField(max_length=500)
