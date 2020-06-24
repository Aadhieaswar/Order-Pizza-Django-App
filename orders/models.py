from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pizza(models.Model):
    pizza = models.CharField(max_length = 64)
    type = models.CharField(max_length = 64)
    size_choices = [
    ('SM', 'Small'),
    ('LG', 'Large')
    ]
    size = models.CharField(max_length = 2, choices = size_choices)
    cost = models.FloatField(blank = False)

class Toppings(models.Model):
    topping = models.CharField(max_length = 64)

class Subs(models.Model):
    sub = models.CharField(max_length = 64)
    size_choices = [
    ('SM', 'Small'),
    ('LG', 'Large')
    ]
    size = models.CharField(max_length = 2, choices = size_choices)
    cost = models.FloatField(blank = False)

class Pastas(models.Model):
    pasta = models.CharField(max_length = 64)
    cost = models.FloatField(blank = False)

class Salads(models.Model):
    salad = models.CharField(max_length = 64)
    cost = models.FloatField(blank = False)

class DinnerPlatters(models.Model):
    platter = models.CharField(max_length = 64)
    size_choices = [
    ('SM', 'Small'),
    ('LG', 'Large')
    ]
    size = models.CharField(max_length = 2, choices = size_choices)
    cost = models.FloatField(blank = False)

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
