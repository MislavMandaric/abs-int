from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django.forms import CharField
from datetime import date
from django import forms


class CustomAuthenticationForm(AuthenticationForm):
  username = CharField(widget=TextInput(attrs={'class':'form-control'}))
  password = CharField(widget=PasswordInput(attrs={'class':'form-control'})) 


class SearchForm(forms.Form):
	tags = CharField(widget=TextInput(attrs={'class':'form-control'}))
	cat1 = BooleanField(required=False)
	cat2 = BooleanField(required=False)




