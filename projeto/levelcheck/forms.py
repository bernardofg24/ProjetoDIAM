from django import forms
from .models import Game, Genre, Character, Article

# Create your forms here.


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = '__all__'


class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = '__all__'


class CharacterForm(forms.ModelForm):

    class Meta:
        model = Character
        exclude = ('pub_date',)


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ('pub_date',)
