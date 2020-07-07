from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection
from django.db.models import Q

from decimal import *

from .forms import CreateUser
from .decorators import Unauthenticated_user, Authenticated_user
from .models import *

# Create your views here.

Menu = {
'pizza': Pizza.objects.all(),
'salad': Salad.objects.all(),
'sub': Sub.objects.all(),
'dinnerplatter': DinnerPlatter.objects.all(),
'pasta': Pasta.objects.all(),
'topping': Topping.objects.all(),
'SubAdd': SubAdditional.objects.all(),
}

def index(request):

    if request.session.get("user") is not None:
        user = "Welcome " + request.session["user"] + "!"
    else:
        user = ""

    context = {
    'msg': user,
    'pizzas': Menu['pizza'],
    'subs': Menu['sub'],
    'pastas': Menu['pasta'],
    'dinner_platters': Menu['dinnerplatter'],
    'salads': Menu['salad'],
    'toppings': Menu['topping'],
    'sub_add': Menu['SubAdd'],
    }
    return render(request, "orders/index.html", context)

@Unauthenticated_user
def login_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            name = user.username
            request.session["user"] = name

            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.warning(request, 'Invalid Credentials!')
            return render(request, "orders/login.html")

    return render(request, "orders/login.html")

@Unauthenticated_user
def signup_view(request):

    form = CreateUser()

    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {
    'form': form,
    }

    return render(request, "orders/signup.html", context)

def _logout(request):

    logout(request)
    request.session.clear()

    return redirect("home")

@Authenticated_user
def cart(request):

    cart_items = []

    person = request.user.id

    try: 
        query = f"SELECT * FROM orders_cart WHERE customer_id = {person}"

        for items in Cart.objects.raw(query):
            cart_items.append(items)
    except: 
        pass

    context = {
    'pizzas': Menu['pizza'],
    'subs': Menu['sub'],
    'pastas': Menu['pasta'],
    'dinner_platters': Menu['dinnerplatter'],
    'salads': Menu['salad'],
    'toppings': Menu['topping'],
    'sub_add': Menu['SubAdd'],
    'cart_items': cart_items,
    }

    return render(request, "orders/cart.html", context)

@Authenticated_user
def submit_order(request):

    if request.method == "POST":

        # form input to get the item type
        itemType = request.POST["itemType"]

        # form input for cheese pizza
        cheeseSize = request.POST["cheeseSize"]
        cheeseType = request.POST["cheeseType"]

        # form input for pizza
        pizzaType = request.POST["pizzaType"]
        pizzaSize = request.POST["pizzaSize"]
        topping1 = request.POST["topping1"]
        topping2 = request.POST["topping2"]
        topping3 = request.POST["topping3"]

        # form input for special pizza
        specialSize = request.POST["specialSize"]
        specialType = request.POST["specialType"]

        # form input for sub
        subType = request.POST["subType"]
        subSize = request.POST["subSize"]
        subExtras = request.POST["subExtras"]

        # form input for pasta
        pastaType = request.POST["pastaType"]

        # form input for salad
        saladType = request.POST["saladType"]

        # form input for Dinner Platter
        DPType = request.POST["DPType"]
        DPSize = request.POST["DPSize"]

        query = connection.cursor()

        # if loop to get and add cheese pizza to the cart
        if (itemType == "Cheese"):
            try:
                item = Pizza.objects.values_list(f'{cheeseSize}', flat=True).filter(Q(pizza=itemType), Q(type=cheeseType))
                cPrice = item[0]
                cheeseSize = cheeseSize.capitalize()

                # add item to the cart table 
                cheese_pizza = Cart(customer=request.user, item=f"{cheeseType} {itemType} Pizza - {cheeseSize}", price=cPrice)
                cheese_pizza.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!')
                return redirect("cart")

        # if loop to get and add special pizza to the cart
        elif (itemType == "Special"):
            try:
                item = Pizza.objects.values_list(f'{specialSize}', flat=True).filter(Q(pizza=itemType), Q(type=specialType))
                sPrice = item[0]
                specialSize = specialSize.capitalize()
                
                # add item to the cart table
                special_pizza = Cart(customer=request.user, item=f"{specialType} {itemType} Pizza - {specialSize}", price=sPrice)
                special_pizza.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!')
                return redirect("cart")

        # if loop to get and add customized pizza to the cart
        elif (itemType == "Pizza"): 
            try:
                i = 0
                topArray = [topping1, topping2, topping3]
                for top in topArray:
                    if (top != "none"):
                        i += 1
                    else:
                        top = ""
                
                if (i == 1):
                    pizza_topping = "1-Topping"
                else:
                    pizza_topping = f"{i}-Toppings"

                item = Pizza.objects.values_list(f'{pizzaSize}', flat=True).filter(Q(pizza=pizza_topping), Q(type=pizzaType))
                pPrice = item[0]

                pizzaSize = pizzaSize.capitalize()

                # add item to the cart table
                if (pizza_topping == "1-Topping"):
                    custom_pizza = Cart(customer=request.user, item=f"{pizzaType} Pizza with {topArray[0]} - {pizzaSize}", price=pPrice)
                elif (pizza_topping == "2-Toppings"):
                    custom_pizza = Cart(customer=request.user, item=f"{pizzaType} Pizza with {topArray[0]} and {topArray[1]} - {pizzaSize}", price=pPrice)
                else:
                    custom_pizza = Cart(customer=request.user, item=f"{pizzaType} Pizza with {topArray[0]}, {topArray[1]}, and {topArray[2]} - {pizzaSize}", price=pPrice)
                custom_pizza.save()

            except: 
                messages.error(request, 'Please Submit a Valid Order!')
                return redirect("cart")

    return redirect("cart")
