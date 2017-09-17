from .models import Game


def categories(request):
    return {
        'games': Game.objects.all()
    }
