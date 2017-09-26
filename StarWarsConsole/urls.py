from django.conf.urls import url
from . import views
from StarWarsConsole.views import register, register_success, logout_page, home, authlogin, login_juego, register_juego

urlpatterns = [
    url(r'^logout/$', logout_page, name='logout_page'),
#    url(r'^log_in/$', login, name='log_in'),
    url(r'^accounts/login/$', authlogin, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^register/success/$', register_success, name='register_success'),
    url(r'^home/$', home, name='home'),
    url(r'^login_juego/$', login_juego),
    url(r'^register_juego/$', register_juego),
]
