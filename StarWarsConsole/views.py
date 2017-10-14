from django.shortcuts import render

# Create your views here.
from StarWarsConsole.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse
from StarWarsConsole.models import Usuario
from django.contrib.auth.models import User
import json
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
import requests
from requests.auth import HTTPBasicAuth

@csrf_protect
def register(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['usuario'],
            password=form.cleaned_data['clave'],
            )
            user.save()
            usuario = Usuario.objects.create(
            user=user,
            tipo="administrador",
            )
            return HttpResponseRedirect('/StarWarsConsole/register/success/')
    else:
        form=RegistrationForm()
    variables={
    'form':form
    }
    template = get_template('register.html')
    return HttpResponse(template.render(variables,request))

def authlogin(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['usuario']
            password = form.cleaned_data['clave']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/StarWarsConsole/home/')
            else:
                return HttpResponseRedirect('/StarWarsConsole/accounts/login/')
    else:
        form=LoginForm()
    variables={
    'form':form
    }
    template = get_template('login.html')
    return HttpResponse(template.render(variables,request))

@api_view(['POST'])
def register_juego(request, json_request):
    if request.method == 'POST':
        jsondict = request.data
        usuario = jsondict['id']
        password = jsondict['password']
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            temp = "false"
        else:
            temp = "true"
            user1 = User.objects.create_user(
            username=usuario,
            password=clave,
            )
            user1.save()
            usuario1 = Usuario.objects.create(
            user=user1,
            tipo="jugador",
            )
        jsonreturn = [{"result":temp}]
        return JsonResponse(jsonreturn, safe=False)

@api_view(['POST'])
def login_juego(request):
    if request.method == 'POST':
        jsondict = request.data
        usuario = jsondict['id']
        password = jsondict['password']
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            temp = "true"
        else:
            temp = "false"
        jsonreturn = [{"result":temp}]
        return JsonResponse(jsonreturn, safe=False)

def register_success(request):
    template = get_template('register_success.html')
    variables = {}
    return HttpResponse(template.render(variables, request))

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/StarWarsConsole/accounts/login/')

@login_required
def home(request):
    user=request.user
    usuario=Usuario.objects.get(user=user.id)
    variables={
    'user': user,
    'usuario': usuario.user.username,
    'tipo': usuario.tipo,
    }
    template = get_template('home.html')
    return HttpResponse(template.render(variables, request))
