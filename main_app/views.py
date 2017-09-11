# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import TextInput, FileInput
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from datetime import date

from .forms import LoginForm, RegistrationForm, CreateGameForm, RegisterOnGameForm

from .models import Game, User, Participants


def index(request):
    return render(request, 'index.html')


def profile(request):
    current_user = User.objects.get(username = request.user)
    games = Game.objects.all()
    killer = Participants.objects.filter(user = current_user)
    return render(request, 'profile.html',
                  {'current_user': current_user,
                   'games': games,
                   'killer': killer})


def rules(request):
    return render(request, 'rules.html')


def nominations(request):
    return render(request, 'nominations.html')


def statistics(request):
    killers = Participants.objects.all()
    return render(request, 'statistics.html', {'killers': killers})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/profile/')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('profile/')
                else:
                    print("Аккаунт был отключен!")
            else:
                error_message = "Пользователя с таким логином и паролем не существует!"
    elif request.user.is_authenticated:
        return HttpResponseRedirect('profile/')
    else:
        form = LoginForm()
    return render(request, 'index.html', {'form': form, 'error_message': error_message})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def createGame(request):
    error_message = None
    games = Game.objects.all()
    killer = Participants.objects.filter(user = current_user)
    if request.method == 'POST':
        form = CreateGameForm(data = request.POST)
        if form.is_valid():
            game = form.save(commit = False)
            try:
                game.save()
                return HttpResponseRedirect('/profile/')
            except:
                error_message = 'Ошибка при создании игры'
    else:
        form = CreateGameForm()
    return render(request, 'profile-create-game.html', {'form': form,
                                                        'error_message': error_message,
                                                        'games': games,
                                                        'killer': killer})

def manageGame(request, game_id):
    # game_name = get_object_or_404(Game.objects, game_name=game_name)
    current_game = Game.objects.get(id=game_id)
    games = Game.objects.all()
    killer = Participants.objects.filter(user = current_user)
    return render(request, 'profile-manage-game.html', {'games': games,
                                                        'current_game': current_game,
                                                        'killer': killer})

def startRegistration(request):
    game_id = request.POST.get('game_id', None)
    if (game_id):
        game = Game.objects.get(id=game_id)
        if game is not None:
            game.start_date = date.today()
            game.save()
        return HttpResponse(date.today())


def registerOnGame(request, game_id):
    gameid = Game.objects.get(pk=game_id)
    games = Game.objects.all()
    killer = User.objects.get(username=request.user)
    if request.method == "POST":
        form = RegisterOnGameForm(data = request.POST, files = request.FILES)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            participant = form.save(commit = False)
            participant.user = killer
            participant.participants = gameid
            participant.first_name = killer.first_name
            participant.last_name = killer.last_name
            participant.save()
            return HttpResponseRedirect('/profile/')
    else:
        form  = RegisterOnGameForm()
    return render(request, 'profile-register-on-game.html', {'form': form,
                                                             'games': games})
