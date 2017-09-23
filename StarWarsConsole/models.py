from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Usuario(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    tipo=models.Charfield(max_length=13)
