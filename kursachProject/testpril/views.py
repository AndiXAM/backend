from django.shortcuts import render, redirect
from .models import Tournament, Game
from .forms import RegistrationForm
from .models import Tournament, Team, Player
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate
from .forms import CustomLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .serializers import TournamentSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

def create_tournament(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        game_name = request.POST.get('game_name')
        max_player_count = int(request.POST.get('max_player_count'))
        date = request.POST.get('date')

        game, created = Game.objects.get_or_create(name=game_name)

        tournament = Tournament(name=name, game=game, player_count=0, max_player_count=max_player_count, date=date)
        tournament.save()

        team_a = Team.objects.create(name='Team A', game=game)
        team_b = Team.objects.create(name='Team B', game=game)

        tournament.teams.add(team_a, team_b)

        return redirect('tournament_list')

    return render(request, 'tournaments/create.html')



@api_view(['GET','POST'])
def tournament_list_s(request):


    if request.method == 'GET':
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(tournaments,many=True)
        return JsonResponse(serializer.data, safe = False)

    elif request.method == 'POST':
        serializer = TournamentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT', 'DELETE'])
def tournament_list_s_detail(request, tournament_id):

    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except Tournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TournamentSerializer(tournament)
        return JsonResponse(serializer.data, safe = False)

    elif request.method == 'PUT':
        serializer = TournamentSerializer(tournament, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        tournament.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def tournament_list(request):
    tournaments = Tournament.objects.all()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tournament_list')
    else:
        form = AuthenticationForm()

    return render(request, 'tournaments/list.html', {'tournaments': tournaments, 'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tournament_list')
    else:
        form = RegistrationForm()
    return render(request, 'register/register.html', {'form': form})


def select_team(request, tournament_id):
    try:
        tournament = Tournament.objects.get(id=tournament_id)
    except ObjectDoesNotExist:
        return redirect('tournament_list')

    teams = tournament.teams.all()

    if request.method == 'POST':
        selected_team_id = request.POST.get('team')
        selected_team = Team.objects.get(id=selected_team_id)


        player, created = Player.objects.get_or_create(
            name=request.user.username,
            surname='',
            country='',
            game=tournament.game,
        )


        current_team = None
        for team in tournament.teams.all():
            if player in team.players.all():
                current_team = team
                break

        if current_team:

            current_team.players.remove(player)

        selected_team.players.add(player)


        unique_players = set()
        for team in tournament.teams.all():
            unique_players.update(team.players.all())

        tournament.player_count = len(unique_players)
        tournament.save()

        return redirect('tournament_list')

    return render(request, 'tournaments/select_team.html', {'tournament': tournament, 'teams': teams})



def tournament_teams(request, tournament_id):
    try:
        tournament = Tournament.objects.get(id=tournament_id)  # Using get() instead of get_object_or_404
    except ObjectDoesNotExist:
        return redirect('tournament_list')

    teams = tournament.teams.all()

    return render(request, 'tournaments/team_list.html', {'tournament': tournament, 'teams': teams})


def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tournament_list')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    if request.method == 'POST':
        logout(request)  # Выход пользователя
        return redirect(request.META.get('HTTP_REFERER', '/'))