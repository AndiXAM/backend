from django import forms
from .models import Tournament
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class TournamentForm(forms.ModelForm):
    game_name = forms.CharField(max_length=100, label='Название игры')  # Field for game name
    player_count = forms.IntegerField(min_value=0, max_value=8, initial=0, label='Количество игроков')
    date = forms.DateTimeField(label='Дата турнира', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Tournament
        fields = ['name', 'player_count', 'date']  # Include player count and date

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)