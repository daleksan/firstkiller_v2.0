# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .forms import LoginForm


def index(request):
    return render(request, 'index.html')


def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile.html',
                  {'username': username})


def rules(request):
    return render(request, 'rules.html')


def nominations(request):
    return render(request, 'nominations.html')


def statistics(request):
    return render(request, 'statistics.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("Аккаунт был отключен!")
            else:
                print("Неправильные логин или пароль!")
    else:
        form = LoginForm()
        return render(request, 'index.html', {'form': form})


# Create your views here.
