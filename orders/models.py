from django.db import models
from django.contrib.auth.models import User

# choice vars
status_choices = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed')
)

# Create your models here.

class Pizza(models.Model):
    pizza = models.CharField(max_length = 64)
    type = models.CharField(max_length = 64)
    small = models.DecimalField(max_digits = 10, decimal_places = 2)
    large = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return f"{self.type} {self.pizza} pizza - Small: ${self.small} - Large: ${self.large}"

class Topping(models.Model):
    topping = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.topping}"


class Sub(models.Model):
    sub = models.CharField(max_length = 64)
    small = models.DecimalField(max_digits = 10, decimal_places = 2)
    large = models.DecimalField(max_digits = 10, decimal_places = 2)
    def __str__(self):
        return f"{self.sub} sub - Small: ${self.small} - Large: ${self.large}"

class SubAdditional(models.Model):
    item = models.CharField(max_length = 64)
    small = models.DecimalField(max_digits = 10, decimal_places = 2)
    large = models.DecimalField(max_digits = 10, decimal_places = 2)
    def __str__(self):
        return f"{self.item} - Small: ${self.small} - Large: ${self.large}"

class Pasta(models.Model):
    pasta = models.CharField(max_length = 64)
    cost = models.DecimalField(max_digits = 10, decimal_places = 2)
    def __str__(self):
        return f"{self.pasta} - ${self.cost}"

class Salad(models.Model):
    salad = models.CharField(max_length = 64)
    cost = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return f"{self.salad} - ${self.cost}"

class DinnerPlatter(models.Model):
    platter = models.CharField(max_length = 64)
    small = models.DecimalField(max_digits = 10, decimal_places = 2)
    large = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return f"{self.platter} - Small: ${self.small} - Large: ${self.large}"

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    item = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.qty} order(s) of {self.item} - ${self.price}"

class Order(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    items = models.ManyToManyField(Cart)
    status = models.CharField(max_length=10, choices=status_choices, default="Pending")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order Created: {self.created}, Status: {self.status}"
