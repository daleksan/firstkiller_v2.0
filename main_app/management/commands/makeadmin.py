from django.core.management.base import BaseCommand, CommandError
from main_app.models import User


class Command(BaseCommand):
    help = 'make <username> admin'

    def add_arguments(self, parser):
        parser.add_argument('usernames', nargs='+', type=str)

    def handle(self, *args, **options):
        for username in options['usernames']:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError('Username "%s" does not exist' % username)

            user.is_admin = True
            user.save()

            self.stdout.write(self.style.SUCCESS('User "%s" successfully promoted to admin' % user))
