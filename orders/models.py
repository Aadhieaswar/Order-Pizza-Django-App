from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pizza(models.Model):
    pizza = models.CharField(max_length = 64)
    type = models.CharField(max_length = 64)
    small = models.DecimalField(max_digits = 4, decimal_places = 2)
    large = models.DecimalField(max_digits = 4, decimal_places = 2)

    def __str__(self):
        return f"{self.type} {self.pizza} pizza - Small: ${self.small} - Large: ${self.large}"

class Topping(models.Model):
    topping = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.topping}"


class Sub(models.Model):
    sub = models.CharField(max_length = 64)
    small = models.DecimalField(max_digits = 4, decimal_places = 2)
    large = models.DecimalField(max_digits = 4, decimal_places = 2)
    def __str__(self):
        return f"{self.sub} sub - Small: ${self.small} - Large: ${self.large}"

class Pasta(models.Model):
    pasta = models.CharField(max_length = 64)
    cost = models.DecimalField(max_digits = 4, decimal_places = 2)
    def __str__(self):
        return f"{self.pasta} - ${self.cost}"

class Salad(models.Model):
    salad = models.CharField(max_length = 64)
    cost = models.DecimalField(max_digits = 4, decimal_places = 2)

    def __str__(self):
        return f"{self.salad} - ${self.cost}"

class DinnerPlatter(models.Model):
    platter = models.CharField(max_length = 64)
    small = models.DecimalField(max_digits = 4, decimal_places = 2)
    large = models.DecimalField(max_digits = 4, decimal_places = 2)

    def __str__(self):
        return f"{self.platter} - Small: ${self.small} - Large: ${self.large}"

#class PizzaCart(models.Model):
#   customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
#    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="pizza")
#    toppping1 = models.ForeignKey(Topping, on_delete=models.CASCADE)
#    toppping2 = models.ForeignKey(Topping, on_delete=models.CASCADE)
#    topping3 = models.ForeignKey(Topping, on_delete=models.CASCADE)
#    total = models.ForegnKey()
