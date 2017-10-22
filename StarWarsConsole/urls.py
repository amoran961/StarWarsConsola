from django.conf.urls import url
from . import views
from StarWarsConsole.views import register, register_success, logout_page, home, authlogin, login_juego, register_juego, configuration, configuration_changed, register_record

urlpatterns = [
    url(r'^logout/$', logout_page, name='logout_page'),
#    url(r'^log_in/$', login, name='log_in'),
    url(r'^accounts/login/$', authlogin, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^register/success/$', register_success, name='register_success'),
    url(r'^configuration/changed/$', configuration_changed, name='configuration_changed'),
    url(r'^home/$', home, name='home'),
    url(r'^configuration/$', configuration, name='configuration'),
    url(r'^login_juego/$', login_juego),
    url(r'^register_juego/$', register_juego),
    url(r'^register_record/$', register_record),
]
