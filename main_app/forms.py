# -*- coding: utf-8 -*-
from django import forms
from .models import User, Game, Participants   # fill in custom user info then save it
# from django.contrib.auth.forms import UserCreationForm
from .admin import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(label=u'Имя пользователя', max_length=64)
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=u'Имя',
                                 max_length=40,
                                 required=True,
                                 help_text='Ваше Имя.',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': u'Введите ваше имя'}))
    last_name = forms.CharField(label=u'Фамилия',
                                max_length=40,
                                required=True,
                                help_text='Ваша Фамилия.',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': u'Введите вашу фамилию'}))
    group_number = forms.CharField(label=u'Номер группы',
                                   max_length=15,
                                   required=True,
                                   help_text='Номер вашей группы.',
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': u'Введите номер группы ("-" для преподавателей)'}))
    mobile_phone = forms.CharField(label=u'Номер телефона',
                                   max_length=40,
                                   required=True,
                                   help_text='Номер мобильного телефона.',
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': u'Введите номер мобильного телефона'}))
    email = forms.EmailField(label=u'Email',
                             max_length=254,
                             required=True,
                             help_text='Ваш электронный почтовый ящик.',
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': u'Введите email'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'mobile_phone', 'group_number', 'email', 'password1', 'password2')


class CreateGameForm(forms.ModelForm):
    game_name = forms.CharField(label='Название',
                                max_length=254,
                                required=True,
                                help_text='Название',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': u'Введите название игры'}))

    class Meta:
        model = Game
        fields = ('game_name',)


class RegisterOnGameForm(forms.ModelForm):
    group_number = forms.CharField(label=u'Номер группы',
                                   max_length=15,
                                   required=True,
                                   help_text='Номер вашей группы.',
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': u'Введите номер группы ("-" для преподавателей)'}))
    photo = forms.ImageField(label=u'Фотография',
                             required=True)

    class Meta:
        model = Participants
        fields = ('group_number', 'photo',)


class ConfirmKillForm(forms.ModelForm):
    victim_code = forms.CharField(label=u'Код',
                                  help_text='Код вашей жертвы.',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': u'Введите код вашей жертвы'}))

    class Meta:
        model = Participants
        fields = ('victim_code',)
