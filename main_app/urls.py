from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user/(\w+)/$', views.profile, name='profile'),
    # url(r'^login/$', views.login_view, name='login'),
    url(r'^$', views.login_view),
    url(r'^rules/$', views.rules),
    url(r'^nominations/$', views.nominations),
    url(r'^statistics/$', views.statistics),
]
