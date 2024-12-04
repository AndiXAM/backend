from django.urls import path
from .views import tournament_list, create_tournament, register, select_team, tournament_teams, user_login, custom_logout

urlpatterns = [
    path('tournaments/', tournament_list, name='tournament_list'),  # Список турниров
    path('tournaments/create/', create_tournament, name='create_tournament'),  # Создание турнира
    path('register/', register, name='register'),
    path('tournaments/<int:tournament_id>/select_team/', select_team, name='select_team'),
    path('tournaments/<int:tournament_id>/teams/', tournament_teams, name='tournament_teams'),  # View teams in a tournament
    path('login/', user_login, name='login'),
    path('logout/', custom_logout, name='logout'),
]