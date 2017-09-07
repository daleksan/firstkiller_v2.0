# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'index.html')

def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile.html',
                  {'username': username})


# Create your views here.
