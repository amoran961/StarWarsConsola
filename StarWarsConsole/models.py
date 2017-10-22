from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Usuario(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    tipo=models.CharField(max_length=13)

class Configuration(models.Model):
    configurationid=models.Charfield(max_length=1)
    mision=models.CharField(max_length=35)
    bando=models.CharField(max_length=10)
    dificultad=models.CharField(max_length=15)

class Record(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    record=models.CharField(max_length=20)
    mision=models.CharField(max_length=35)
    bando=models.CharField(max_length=10)
    dificultad=models.CharField(max_length=15)
