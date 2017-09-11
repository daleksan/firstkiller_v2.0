# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from main_app.models import User


class Command(BaseCommand):
    help = 'make <username> admin'

    def add_arguments(self, parser):
        parser.add_argument('usernames', nargs='+', type=str)

    def handle(self, *args, **options):
        for username in options['usernames']:
            try:
                user = User.objects.get_or_create(username=username,
                                                  first_name = 'test_name',
                                                  last_name = "test_lastname",
                                                  group_number = u"381606-1м",
                                                  email = "test@test.ru",
                                                  mobile_phone = "+79219048192481",
                                                  password1="qwerty",
                                                  password2="qwerty")
            except User.DoesNotExist:
                raise CommandError('Username "%s" does not exist' % username)

            self.stdout.write(self.style.SUCCESS('User "%s" successfully created' % user))
