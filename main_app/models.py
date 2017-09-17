# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from random import randint
import os

from .managers import UserManager
from .constants import KILLER_STATUS_CHOICES, ALIVE, \
                       GAME_STATUS_CHOICES, NEW_GAME


def generate_code(n=6):
    range_start = 10**(n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)


def directory_path(instance, filename):
    return 'files/instance_id_{0}/{1}'.format(instance.pk, filename)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=40, blank=False, unique=True)
    email = models.EmailField(_('email address'), unique=True, blank=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    group_number = models.CharField(_('group number'), max_length=15, blank=False)
    mobile_phone = models.CharField(_('mobile phone'), unique=True, max_length=40, blank=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'group_number', 'mobile_phone', ]

    def __str__(self):
        return self.username

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Game(models.Model):
    game_name = models.CharField(max_length=254, blank=False, unique=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    killers = models.IntegerField(default=0, blank=False)
    status = models.CharField(max_length=24, choices=GAME_STATUS_CHOICES, default=NEW_GAME, unique=True)

    def get_game_status(self):
        return self.status

    def get_game_name(self):
        return self.game_name

    def get_game_start_date(self):
        return self.start_date

    def get_game_end_date(self):
        return self.end_date

    def get_game_killers(self):
        return self.killers


def get_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.personal_code, ext)
    return os.path.join('game/', filename)


class Participants(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    participants = models.ForeignKey(Game, related_name="participants", on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    group_number = models.CharField(max_length=30, blank=False)
    photo = models.ImageField(upload_to=get_file_name)
    status = models.CharField(choices=KILLER_STATUS_CHOICES, max_length=5, default=ALIVE)
    personal_code = models.CharField(default=generate_code, blank=False, max_length=6, unique=True)
    victim_code = models.CharField(default=None, blank=True, null=True, max_length=6)
    victim_mobile_phone = models.CharField(default=None, blank=True, null=True, max_length=40)
    kills = models.IntegerField(default=0)

    def get_game_name(self):
        return self.participants.game_name

    def get_user_info(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        user_info = '%s %s (%s)' % (self.first_name, self.last_name, self.group_number)
        return user_info.strip()

    def get_status(self):
        return self.status

    def get_kills(self):
        return self.kills

    def is_alive(self):
        if self.status == ALIVE:
            return True
        else:
            return False
