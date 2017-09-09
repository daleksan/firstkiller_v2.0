# -*- coding: utf-8 -*-
from django import forms
from .models import User   # fill in custom user info then save it
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(label=u'Имя пользователя', max_length=64)
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=40, required=True, help_text='Ваше Имя.')
    last_name = forms.CharField(max_length=40, required=True, help_text='Ваша Фамилия.')
    group_number = forms.CharField(max_length=15, required=True, help_text='Номер вашей группы.')
    mobile_phone = forms.CharField(max_length=40, required=True, help_text='Номер мобильного телефона.')
    email = forms.EmailField(max_length=254, required=True, help_text='Ваш электронный почтовый ящик.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'mobile_phone', 'email', 'password1', 'password2')
