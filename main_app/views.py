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
    current_user = request.user
    games = Game.objects.all()
    return render(request, 'profile.html',
                  {'current_user': current_user,
                   'games': games})


def rules(request):
    return render(request, 'rules.html')


def nominations(request):
    return render(request, 'nominations.html')


def statistics(request):
    return render(request, 'statistics.html')


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
                                                        'games': games})

def manageGame(request, game_id):
    # game_name = get_object_or_404(Game.objects, game_name=game_name)
    current_game = Game.objects.get(id=game_id)
    games = Game.objects.all()
    return render(request, 'profile-manage-game.html', {'games': games,
                                                        'current_game': current_game})

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
    print killer.first_name
    KillerFormSet = inlineformset_factory(Game,
                                          Participants,
                                          fields=('group_number', 'photo',),
                                          extra=1,
                                          can_delete=False,
                                          labels={'group_number': u'Номер группы',
                                                  'photo': u'Фотография'},
                                          widgets={'group_number': TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': u'Введите номер группы ("-" для преподавателей)'})})
    if request.method == 'POST':
        formset = KillerFormSet(request.POST, request.FILES, instance=gameid)
        if formset.is_valid():
            participant = formset.save(commit = False)
            participant.user = request.user
            participant.first_name = killer.first_name
            participant.last_name = killer.last_name
            participant.save()
            return HttpResponseRedirect('/profile/')
    else:
        formset = KillerFormSet(instance=gameid)
    return render(request, 'profile-register-on-game.html', {'form': formset,
                                                             'games': games})
# Create your views here.
