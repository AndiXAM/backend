from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tournaments = models.ManyToManyField('Tournament', related_name='players')

    def __str__(self):
        return f"{self.name} {self.surname}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    players = models.ManyToManyField(Player, related_name='teams', blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
    player_count = models.IntegerField(default=0)
    max_player_count = models.IntegerField(default=8)
    date = models.DateTimeField()

    def clean(self):
        if self.player_count < 0 or self.player_count > self.max_player_count:
            raise ValidationError('Player count must be between 0 and max player count.')

    def __str__(self):
        return f"{self.name} - {self.game.name}"






