from django import forms
from .models import Game, Genre, Character

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
