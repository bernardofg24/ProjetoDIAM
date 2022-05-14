from django import forms
from .models import Game, Genre

# Create your forms here.


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = '__all__'

