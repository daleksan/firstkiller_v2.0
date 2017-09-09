from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    # url(r'^login/$', views.login_view, name='login'),
    url(r'^$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^rules/$', views.rules, name='rules'),
    url(r'^nominations/$', views.nominations, name='nominations'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^registration/$', views.registration, name='registration'),
]
