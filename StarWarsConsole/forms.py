# This Python file uses the following encoding: utf-8

import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from StarWarsConsole.models import Usuario

class RegistrationForm(forms.Form):
    usuario = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Usuario"), error_messages={ 'invalid': _("Usuario solo puede tener letras, numeros y _.") })
    clave = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Clave"))
    clave_confirmar = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Clave (nuevamente)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['usuario'])
        except User.DoesNotExist:
            return self.cleaned_data['usuario']
        raise forms.ValidationError(_("Usuario ya existe."))

    def clean(self):
        if 'clave' in self.cleaned_data and 'clave_confirmar' in self.cleaned_data:
            if self.cleaned_data['clave'] != self.cleaned_data['clave']:
                raise forms.ValidationError(_("Las claves no coinciden."))
        return self.cleaned_data

class LoginForm(forms.Form):
    usuario = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Usuario"), error_messages={ 'invalid': _("Usuario solo puede tener letras, numeros y _.") })
    clave = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Clave"))

#revisar el campo choices y cleaned data
class ConfigurationForm(forms.Form):
    CHOICESM = [("Asalto a la luna de Endor", "Asalto a la luna de Endor"), ("Ataque a la Estrella de la Muerte", "Ataque a la Estrella de la Muerte")]
    mision = forms.ChoiceField(widget=forms.Select, choices=CHOICESM, label=_("Mision"))
    CHOICESB = [("Rebeldes", "Rebeldes"), ("Imperio", "Imperio")]
    bando = forms.ChoiceField(widget=forms.Select, choices=CHOICESB, label=_("Bando"))
    CHOICESD = [("Fácil", "Fácil"), ("Intermedio", "Intermedio"), ("Difícil", "Difícil")]
    dificultad = forms.ChoiceField(widget=forms.Select, choices=CHOICESD, label=_("Dificultad"))
