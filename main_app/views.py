# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegistrationForm


def index(request):
    return render(request, 'index.html')


def profile(request):
    current_user = request.user
    return render(request, 'profile.html',
                  {'current_user': current_user})


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

# Create your views here.
