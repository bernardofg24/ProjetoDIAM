from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Genres(models.Model):
    genre = models.CharField(max_length=50, primary_key=True)


class Game(models.Model):
    title = models.CharField(max_length=50)
    img_src = models.CharField(max_length=150)
    developer = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    release = models.DateTimeField('Release Date')


class GameGenre(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    img_src = models.CharField(max_length=150)
    favorite_genres = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True)


class UserGames(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Review(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    comment = models.CharField(max_length=500)
