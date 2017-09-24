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
