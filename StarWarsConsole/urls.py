from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
from StarWarsConsole.views import register, register_success, logout_page, home

urlpatterns = [
    url(r'^logout/$', logout_page, name='logout_page'),
    url(r'^log_in/$', login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^register/success/$', register_success, name='register_success'),
    url(r'^home/$', home, name='home')
]
