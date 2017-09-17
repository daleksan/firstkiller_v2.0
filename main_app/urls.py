from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile/$', views.profileView, name='profile'),
    # url(r'^login/$', views.login_view, name='login'),
    url(r'^$', views.loginView, name='login'),
    url(r'^logout/$', views.logoutView, name='logout'),
    url(r'^rules/$', views.rulesView, name='rules'),
    url(r'^nominations/$', views.nominationsView, name='nominations'),
    url(r'^statistics/$', views.statisticsView, name='statistics'),
    url(r'^registration/$', views.registrationView, name='registration'),
    url(r'^profile/createGame/$', views.createGameView, name='createGame'),
    url(r'^manage/(\w+)/$', views.manageGameView, name='manageGame'),
    url(r'^startRegistration/$', views.startRegistrationRequest, name='startRegistration'),
    url(r'^registerOnGame/(?P<game_id>[0-9]+)$', views.registerOnGameView, name='registerOnGame'),
    url(r'^userStatistics/$', views.userStatisticsView, name='userStatistics'),
    url(r'^kill/$', views.confirmKill, name='confirmKill'),
]
