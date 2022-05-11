from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Generos(models.Model):
    genero = models.CharField(max_length=50, primary_key=True)


class Jogo(models.Model):
    nome = models.CharField(max_length=50)
    img_src = models.CharField(max_length=150)
    dev = models.CharField(max_length=50)
    pub = models.CharField(max_length=50)
    release = models.DateTimeField('Release Date')


class GeneroJogo(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    genero = models.ForeignKey(Generos, on_delete=models.CASCADE)


class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    img_src = models.CharField(max_length=150)
    generos_pref = models.ForeignKey(Generos, on_delete=models.SET_NULL, null=True)


class JogosUtilizador(models.Model):
    user = models.OneToOneField(Utilizador, on_delete=models.CASCADE, primary_key=True)
    jogos = models.ForeignKey(Jogo, on_delete=models.CASCADE)


class Review(models.Model):
    user = models.OneToOneField(Utilizador, on_delete=models.CASCADE)
    jogo = models.OneToOneField(Jogo, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    comment = models.CharField(max_length=500)

