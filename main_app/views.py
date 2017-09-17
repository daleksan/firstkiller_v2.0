# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from datetime import date


from .forms import LoginForm, RegistrationForm, CreateGameForm, RegisterOnGameForm, ConfirmKillForm
from .constants import *
from .models import Game, User, Participants


def indexView(request):
    return render(request, 'index.html')


def profileView(request):
    current_user = User.objects.get(username=request.user)
    currentUrl = request.get_full_path()
    games = Game.objects.all()
    try:
        killer = Participants.objects.get(user=current_user)
    except Participants.DoesNotExist:
        killer = None
    return render(request, 'profile.html', locals())


def rulesView(request):
    currentUrl = request.get_full_path()
    return render(request, 'rules.html', locals())


def nominationsView(request):
    currentUrl = request.get_full_path()
    return render(request, 'nominations.html', locals())


def statisticsView(request):
    killers = Participants.objects.all()
    currentUrl = request.get_full_path()
    return render(request, 'statistics.html', locals())


def registrationView(request):
    currentUrl = request.get_full_path()
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
    return render(request, 'registration.html', locals())


def loginView(request):
    error_message = None
    currentUrl = request.get_full_path()
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
    return render(request, 'index.html', locals())


def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/')


def createGameView(request):
    error_message = None
    currentUrl = request.get_full_path()
    games = Game.objects.all()
    try:
        killer = Participants.objects.get(user=request.user)
    except Participants.DoesNotExist:
        killer = None
    if request.method == 'POST':
        form = CreateGameForm(data=request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            try:
                game.save()
                return HttpResponseRedirect('/profile/')
            except:
                error_message = 'Ошибка при создании игры'
    else:
        form = CreateGameForm()
    return render(request, 'profile-create-game.html', locals())


def manageGameView(request, game_id):
    # game_name = get_object_or_404(Game.objects, game_name=game_name)
    current_game = Game.objects.get(id=game_id)
    games = Game.objects.all()
    try:
        killer = Participants.objects.get(user=request.user)
    except Participants.DoesNotExist:
        killer = None
    return render(request, 'profile-manage-game.html', locals())


def startRegistrationRequest(request):
    game_id = request.POST.get('game_id', None)
    if (game_id):
        game = Game.objects.get(id=game_id)
        if game is not None:
            game.start_date = date.today()
            game.save()
        return HttpResponse(date.today())


def registerOnGameView(request, game_id):
    currentUrl = request.get_full_path()
    currentUser = User.objects.get(username=request.user)
    gameid = Game.objects.get(pk=game_id)
    games = Game.objects.all()
    killer = Participants.objects.filter(user=request.user)
    print currentUrl
    if request.method == "POST":
        form = RegisterOnGameForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            participant = form.save(commit=False)
            participant.user = currentUser
            participant.participants = gameid
            participant.first_name = currentUser.first_name
            participant.last_name = currentUser.last_name
            participant.save()
            messages.success(request, 'Вы успешно зарегистрировались на игру!')
            return HttpResponseRedirect('/profile/')
    else:
        form = RegisterOnGameForm()
    return render(request, 'profile-register-on-game.html', locals())


def userStatisticsView(request):
    currentUrl = request.get_full_path()
    killer = Participants.objects.get(user=request.user)
    games = Game.objects.all()
    return render(request, 'profile-user-statistics.html', locals())


def confirmKill(request):
    currentUrl = request.get_full_path()
    current_game = Game.objects.get(status=GAME_BEGIN)
    killer = Participants.objects.get(participants=current_game, user=request.user)
    games = Game.objects.all()
    if request.method == "POST":
        form = ConfirmKillForm(data=request.POST)
        if form.is_valid():
            input_victim_code = form.cleaned_data['victim_code']
            victim = Participants.objects.get(participants=current_game, personal_code=input_victim_code)
            if input_victim_code != killer.victim_code:
                messages.error(request, 'Неправильный код жертвы!')
                return HttpResponseRedirect('/kill/')
            else:
                killer.victim_code = victim.victim_code
                kills = killer.kills + 1
                killer.kills = kills
                victim.status = DEAD
                victim.save()
                killer.save()
            messages.success(request, 'Вы успешно зафиксировали убийство!')
            return HttpResponseRedirect('/userStatistics/')
    else:
        form = ConfirmKillForm()
    return render(request, 'profile-confirm-kill.html', locals())
