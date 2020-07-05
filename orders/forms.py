from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class OrderPizza(forms.Form):
    pizza_choices = Pizza.objects.values('pizza')
    pizza = forms.ChoiceField(choices=pizza_choices)
    type_choices = ['Regular', 'Sicilian']
    type = forms.ChoiceField(choices=type_choices)
