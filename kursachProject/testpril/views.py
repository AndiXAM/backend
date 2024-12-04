from django.shortcuts import render, redirect
from .models import Tournament, Game
from .forms import TournamentForm
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import Tournament, Team, Player
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate
from .forms import CustomLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

def create_tournament(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        game_name = request.POST.get('game_name')
        max_player_count = int(request.POST.get('max_player_count'))  # Get max player count from form
        date = request.POST.get('date')

        game, created = Game.objects.get_or_create(name=game_name)

        # Create new tournament instance with specified max player count
        tournament = Tournament(name=name, game=game, player_count=0, max_player_count=max_player_count, date=date)
        tournament.save()

        # Create two default teams for the tournament and associate them
        team_a = Team.objects.create(name='Team A', game=game)
        team_b = Team.objects.create(name='Team B', game=game)

        # Associate teams with the tournament
        tournament.teams.add(team_a, team_b)

        return redirect('tournament_list')

    return render(request, 'tournaments/create.html')


def tournament_list(request):
    tournaments = Tournament.objects.all()  # Get all tournaments

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  # Create a form instance with POST data
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('tournament_list')  # Redirect to the tournament list after login
    else:
        form = AuthenticationForm()  # Create an empty form for GET requests

    return render(request, 'tournaments/list.html', {'tournaments': tournaments, 'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('tournament_list')  # Redirect to the tournament list page
    else:
        form = RegistrationForm()
    return render(request, 'register/register.html', {'form': form})


def select_team(request, tournament_id):
    try:
        tournament = Tournament.objects.get(id=tournament_id)  #
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
        return redirect('tournament_list')  # Redirect if tournament does not exist

    teams = tournament.teams.all()  # Get all teams associated with the tournament

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
                return redirect('tournament_list')  # Redirect to the tournament list after successful login
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    if request.method == 'POST':
        logout(request)  # Выход пользователя
        return redirect(request.META.get('HTTP_REFERER', '/'))