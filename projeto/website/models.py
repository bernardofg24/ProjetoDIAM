from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User

class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img_src = models.CharField(max_length=150)

class JogosUtilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Jogos(models.Model):
    jogos_user = models.ForeignKey(JogosUtilizador, on_delete=models.CASCADE)

    nome = models.CharField(max_length=50)
    img_src = models.CharField(max_length=150)
    dev = models.CharField(max_length=50)
    pub = models.CharField(max_length=50)
    release = models.DateTimeField('release date')

class Generos(models.Model):
    generos_pref = models.ForeignKey(Utilizador, on_delete=models.SET_NULL, null=True)
    genero_jogo = models.OneToOneField(Jogos, on_delete=models.RESTRICT)

    genero = models.CharField(max_length=50)

class Review(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jogo = models.OneToOneField(Jogos, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    comment = models.CharField(max_length=500)
