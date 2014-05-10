from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput, Textarea, ClearableFileInput
from django.forms import CharField, BooleanField, MultipleChoiceField, CheckboxSelectMultiple, FileField
from datetime import date
from django import forms

from .models import Category

class CustomAuthenticationForm(AuthenticationForm):
  username = CharField(widget=TextInput(attrs={'class':'form-control'}))
  password = CharField(widget=PasswordInput(attrs={'class':'form-control'}))

class SearchForm(forms.Form):
	tags = CharField(widget=TextInput(attrs={'class':'form-control'}))

	def __init__(self, *args, **kw):
		super(SearchForm, self).__init__(*args, **kw)
		categories = Category.objects.all()
		OPTIONS = []
		for c in categories:
			OPTIONS.append((c.name, c.name))
		self.fields['categories'] = MultipleChoiceField(widget=CheckboxSelectMultiple(attrs={'class':'form-control'}), \
			choices=OPTIONS, label="Kategorija")

class ReceiptForm(forms.Form):
    title = CharField(widget=TextInput(attrs={'class':'form-control'}))
    text = CharField(widget=Textarea(attrs={'class':'form-control'}))
    image = FileField(widget=ClearableFileInput(attrs={'class':'form-control'}))
    tags = CharField(widget=TextInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kw):
        super(SearchForm, self).__init__(*args, **kw)
        categories = Category.objects.all()
        OPTIONS = []
        for c in categories:
            OPTIONS.append((c.name, c.name))
        self.fields['categories'] = MultipleChoiceField(widget=CheckboxSelectMultiple(attrs={'class':'form-control'}), \
            choices=OPTIONS, label="Kategorija")