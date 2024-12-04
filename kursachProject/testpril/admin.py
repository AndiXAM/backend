from django.contrib import admin
from .models import Game, Player, Team, Tournament

# Регистрация моделей в административном интерфейсе
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Tournament)
