from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pizza(models.Model):
    pizza = models.CharField(max_length = 64)
    type = models.CharField(max_length = 64)
    size_choices = [
    ('Small', 'SM'),
    ('Large', 'LG')
    ]
    size = models.CharField(max_length = 5, choices = size_choices)
    cost = models.FloatField(blank = False)

    def __str__(self):
        return f"{self.type} {self.pizza} pizza - {self.size} - ${self.cost}"

class Topping(models.Model):
    topping = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.topping}"


class Sub(models.Model):
    sub = models.CharField(max_length = 64)
    size_choices = [
    ('Small', 'SM'),
    ('Large', 'LG')
    ]
    size = models.CharField(max_length = 5, choices = size_choices)
    cost = models.FloatField(blank = False)

    def __str__(self):
        return f"{self.sub} sub - {self.size} - ${self.cost}"

class Pasta(models.Model):
    pasta = models.CharField(max_length = 64)
    cost = models.FloatField(blank = False)

    def __str__(self):
        return f"{self.pasta} - ${self.cost}"

class Salad(models.Model):
    salad = models.CharField(max_length = 64)
    cost = models.FloatField(blank = False)

    def __str__(self):
        return f"{self.salad} - ${self.cost}"

class DinnerPlatter(models.Model):
    platter = models.CharField(max_length = 64)
    size_choices = [
    ('Small', 'SM'),
    ('Large', 'LG')
    ]
    size = models.CharField(max_length = 5, choices = size_choices)
    cost = models.FloatField(blank = False)

    def __str__(self):
        return f"{self.platter} - {self.size} - ${self.cost}"

#class Cart(models.Model):
#    user = models.ForeignKey(User, on_delete = models.CASCADE)
#    date_ordered = models.DateTimeField(auto_now_add=True)
#    item_choices = [
#    ('Pizza', 'PIZ'),
#    ('Sub', 'SUB'),
#    ('Pasta', 'PAS'),
#    ('Salad', 'SAL'),
#    ('DinnerPlatter', 'DPL')
#    ]
#    item_type = models.CharField(max_length = 3, choices = item_choices, blank=False, null=False)
#    item = models.ForeignKey(self.item_type, on_delete = models.SET_NULL)


#class Order(models.Model):
#    user = models.ForeignKey(User, on_delete = models.CASCADE)
