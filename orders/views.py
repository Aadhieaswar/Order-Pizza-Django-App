from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.db import connection

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

    totalCost = 0

    count = 0

    HST = Decimal(1.08)

    person_id = request.user.id

    try:
        for items in Cart.objects.filter(Q(customer=request.user)):
            count += 1
            cart_items.append(items)

        for price in Cart.objects.values_list('price', flat=True).filter(Q(customer=request.user)):
            totalCost += price

        CostAfterInterest = Decimal("%.2f" % (totalCost * HST))
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
    'price': CostAfterInterest,
    'count': count,
    }

    return render(request, "orders/cart.html", context)

# used to filter out empty toppings in the /add_to_cart/ url
def removeNoneObjects(strObj):
    if (len(strObj) != 4):
        return True
    else: 
        return False 

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

                topArray = list(filter(removeNoneObjects, topArray))

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

        # if loop to get and add subs to the cart table
        elif (itemType == "Sub"):
            try:
                item = Sub.objects.values_list(f'{subSize}', flat=True).filter(Q(sub=subType))
                sPrice = item[0]

                if (subExtras != "none"):
                    extra = SubAdditional.objects.values_list(f'{subSize}', flat=True).filter(Q(item=subExtras))
                    sPrice += extra[0]
                    subSize = subSize.capitalize()

                    # add the item to the cart (with extras for the sub)
                    sub = Cart(customer=request.user, item=f"{subType} Sub with {subExtras} - {subSize}", price=sPrice)
                    sub.save()
                else:
                    subSize = subSize.capitalize()

                    # add the item to the cart (without extras for the sub)
                    sub = Cart(customer=request.user, item=f"{subType} Sub - {subSize}", price=sPrice)
                    sub.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!')
                return redirect("cart")

        # if loop to get or add pasta to the cart table
        elif (itemType == "Pasta"):
            try:
                item = Pasta.objects.values_list('cost', flat=True).filter(Q(pasta=pastaType))
                pasPrice = item[0]

                # add the item to the cart
                pasta = Cart(customer=request.user, item=f"{pastaType} Pasta", price=pasPrice)
                pasta.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!')
                return redirect("cart")
        
        # if loop to get orr add salad to the cart table
        elif (itemType == "Salad"):
            try:
                item = Salad.objects.values_list('cost', flat=True).filter(Q(salad=saladType))
                salPrice = item[0]

                # add the item to the cart
                salad = Cart(customer=request.user, item=f"{saladType} (Salad)", price=salPrice)
                salad.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!')
                return redirect("cart")

        # if loop to get or add dinner platters to the cart table
        elif (itemType == "DinnerPlatter"):
            try:
                item = DinnerPlatter.objects.values_list(f'{DPSize}', flat=True).filter(Q(platter=DPType))
                DPPrice = item[0]
                DPSize = DPSize.capitalize()

                # add the item to the cart
                platter = Cart(customer=request.user, item=f"{DPType} Platter - {DPSize}", price=DPPrice)
                platter.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!')
                return redirect("cart")
                
        # else loop as a layer of protection against the misuse of the HTML form
        else:
            return HttpResponse("ERROR 404 NOT FOUND")

    return redirect("cart")

@Authenticated_user
def checkOut(request):

    if request.method == "POST":
        pass

    return ("cart")
