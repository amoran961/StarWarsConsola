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
from StarWarsConsole.models import Usuario, Configuration, Record
from django.contrib.auth.models import User
import json
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes

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

@login_required
def configuration(request):
    if request.method == 'POST':
        form=ConfigurationForm(request.POST)
        if form.is_valid():
            configuration=Configuration.objects.filter(id=1)
            if not configuration:
                configurationtemp=Configuration.objects.create(
                mision=form.cleaned_data['mision'],
                bando=form.cleaned_data['bando'],
                dificultad=form.cleaned_data['dificultad'],
                )
            else:
                configuration=Configuration.objects.get(id=1)
                configuration.mision = form.cleaned_data['mision']
                configuration.bando = form.cleaned_data['bando']
                configuration.dificultad = form.cleaned_data['dificultad']
                configuration.save()
            return HttpResponseRedirect('/StarWarsConsole/configuration/changed/')
    else:
        form=ConfigurationForm()
    variables={
    'form':form
    }
    template=get_template('configuration.html')
    return HttpResponse(template.render(variables,request))

def configuration_changed(request):
    template = get_template('configuration_changed.html')
    variables = {}
    return HttpResponse(template.render(variables, request))

@api_view(['POST'])
def register_juego(request):
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
            password=password,
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
            configuration=Configuration.objects.get(id=1)
            mision=configuration.mision
            bando=configuration.bando
            dificultad=configuration.dificultad
            temp="true"
            jsonreturn = [{"result":temp, "mision":mision, "bando":bando, "dificultad":dificultad}]
        else:
            temp="false"
            jsonreturn = [{"result":temp}]
        return JsonResponse(jsonreturn, safe=False)

@api_view(['POST'])
def register_record(request):
    if request.method == 'POST':
        jsondict = request.data
        usuario = jsondict['id']
        record = jsondict['record']
        usuariotemp = User.objects.get(username=usuario)
        record=Record.objects.create(
        user=usuariotemp,
        record=record,
        )
        temp = "true"
        jsonreturn = [{"result":temp}]
        return JsonResponse(jsonreturn, safe=False)

@api_view(['POST'])
def ranking(request):
    if request.method == 'POST':
        ranking_temp = Record.objects.all()
        for r in ranking_temp:
            r.record = int(r.record)
        sorted(ranking_temp, key=attrgetter("record"),reverse=True)
        ranking_temp = Record.objects.order_by("-record")
#        for r in ranking_temp:
            r.record = str(r.record)
        total = len(ranking_temp)
        i = 0
        ranking = []
        if total == 0:
            temp="false"
            jsonreturn = [{"result":temp}]
        else:
            if total < 11:
                for record in ranking_temp:
                    i=i+1
                    ranking.append(i)
                    ranking.append(record.user.username)
                    ranking.append(record.record)
            else:
                for record in ranking_temp:
                    if i < 10:
                        i=i+1
                        ranking.append(i)
                        ranking.append(record.user.username)
                        ranking.append(record.record)
            temp="true"
            jsonreturn = [{"result":temp, "total":i, "ranking":ranking}]
        return JsonResponse(jsonreturn, safe=False)

def enviar_record(request):
    pass

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
    configuration=Configuration.objects.get(id=1)
    variables={
    'user': user,
    'usuario': usuario.user.username,
    'tipo': usuario.tipo,
    'mision': configuration.mision,
    'bando': configuration.bando,
    'dificultad': configuration.dificultad,
    }
    template = get_template('home.html')
    return HttpResponse(template.render(variables, request))
