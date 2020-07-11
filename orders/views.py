from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.db import connection

import json
from decimal import *

from .forms import CreateUser
from .decorators import Unauthenticated_user, Authenticated_user
from .models import *

# global vars
Menu = {
'pizza': Pizza.objects.all(),
'salad': Salad.objects.all(),
'sub': Sub.objects.all(),
'dinnerplatter': DinnerPlatter.objects.all(),
'pasta': Pasta.objects.all(),
'topping': Topping.objects.all(),
'SubAdd': SubAdditional.objects.all(),
}

# Create your views here.

def index(request):

    if request.session.get("user") is not None:
        count = Cart.objects.filter(Q(customer=request.user)).count()
    else:
        count = 0

    if (count == 0):
        count_message = "Your cart is empty"
    else:
        count_message = f"You have {count} item(s) in your cart"


    context = {
    'pizzas': Menu['pizza'],
    'subs': Menu['sub'],
    'pastas': Menu['pasta'],
    'dinner_platters': Menu['dinnerplatter'],
    'salads': Menu['salad'],
    'toppings': Menu['topping'],
    'sub_add': Menu['SubAdd'],
    'count': count,
    'count_message': count_message,
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
            messages.info(request, f"Welcome {request.user}!", fail_silently=True)
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
            messages.info(request, f"Welcome {request.user}!", fail_silently=True)
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
            cart_items.append(items)

        for items in Cart.objects.values_list('qty', flat=True).filter(Q(customer=request.user)):
            count += items

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

        # form input to get quantity of the item
        item_quantity = request.POST["item_quantity"] 
        # have a decimal value of the item to perform operations 
        decimal_quantity = Decimal(item_quantity)

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
                cPrice = (item[0]  *  decimal_quantity)
                cheeseSize = cheeseSize.capitalize()

                # add item to the cart table 
                cheese_pizza = Cart(customer=request.user, item=f"{cheeseType} {itemType} Pizza - {cheeseSize}", price=cPrice, qty=item_quantity)
                cheese_pizza.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!', fail_silently=True)
                return redirect("cart")

        # if loop to get and add special pizza to the cart
        elif (itemType == "Special"):
            try:
                item = Pizza.objects.values_list(f'{specialSize}', flat=True).filter(Q(pizza=itemType), Q(type=specialType))
                sPrice = (item[0]  *  decimal_quantity)
                specialSize = specialSize.capitalize()
                
                # add item to the cart table
                special_pizza = Cart(customer=request.user, item=f"{specialType} {itemType} Pizza - {specialSize}", price=sPrice, qty=item_quantity)
                special_pizza.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!', fail_silently=True)
                return redirect("cart")

        # if loop to get and add customized pizza to the cart
        elif (itemType == "Pizza"): 
            try:
                i = 0
                topArray = [topping1, topping2, topping3]
                
                # removes repeated toppings
                topArray = list(dict.fromkeys(topArray))

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
                pPrice = (item[0]  *  decimal_quantity) 

                pizzaSize = pizzaSize.capitalize()

                topArray = list(filter(removeNoneObjects, topArray))

                # add item to the cart table
                if (pizza_topping == "1-Topping"):
                    custom_pizza = Cart(customer=request.user, item=f"{pizzaType} Pizza with {topArray[0]} - {pizzaSize}", price=pPrice, qty=item_quantity)
                elif (pizza_topping == "2-Toppings"):
                    custom_pizza = Cart(customer=request.user, item=f"{pizzaType} Pizza with {topArray[0]} and {topArray[1]} - {pizzaSize}", price=pPrice, qty=item_quantity)
                else:
                    custom_pizza = Cart(customer=request.user, item=f"{pizzaType} Pizza with {topArray[0]}, {topArray[1]}, and {topArray[2]} - {pizzaSize}", price=pPrice, qty=item_quantity)
                custom_pizza.save()

            except: 
                messages.error(request, 'Please Submit a Valid Order!', fail_silently=True)
                return redirect("cart")

        # if loop to get and add subs to the cart table
        elif (itemType == "Sub"):
            try:
                item = Sub.objects.values_list(f'{subSize}', flat=True).filter(Q(sub=subType))
                sPrice = (item[0]  *  decimal_quantity)

                if (subExtras != "none"):
                    extra = SubAdditional.objects.values_list(f'{subSize}', flat=True).filter(Q(item=subExtras))
                    sPrice += extra[0]
                    subSize = subSize.capitalize()

                    # add the item to the cart (with extras for the sub)
                    sub = Cart(customer=request.user, item=f"{subType} Sub with {subExtras} - {subSize}", price=sPrice, qty=item_quantity)
                    sub.save()
                else:
                    subSize = subSize.capitalize()

                    # add the item to the cart (without extras for the sub)
                    sub = Cart(customer=request.user, item=f"{subType} Sub - {subSize}", price=sPrice, qty=item_quantity)
                    sub.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!', fail_silently=True)
                return redirect("cart")

        # if loop to get or add pasta to the cart table
        elif (itemType == "Pasta"):
            try:
                item = Pasta.objects.values_list('cost', flat=True).filter(Q(pasta=pastaType))
                pasPrice = (item[0]  *  decimal_quantity)

                # add the item to the cart
                pasta = Cart(customer=request.user, item=f"{pastaType} Pasta", price=pasPrice, qty=item_quantity)
                pasta.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!', fail_silently=True)
                return redirect("cart")
        
        # if loop to get orr add salad to the cart table
        elif (itemType == "Salad"):
            try:
                item = Salad.objects.values_list('cost', flat=True).filter(Q(salad=saladType))
                salPrice = (item[0]  *  decimal_quantity)

                # add the item to the cart
                salad = Cart(customer=request.user, item=f"{saladType} (Salad)", price=salPrice, qty=item_quantity)
                salad.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!', fail_silently=True)
                return redirect("cart")

        # if loop to get or add dinner platters to the cart table
        elif (itemType == "DinnerPlatter"):
            try:
                item = DinnerPlatter.objects.values_list(f'{DPSize}', flat=True).filter(Q(platter=DPType))
                DPPrice = (item[0]  *  decimal_quantity)
                DPSize = DPSize.capitalize()

                # add the item to the cart
                platter = Cart(customer=request.user, item=f"{DPType} Platter - {DPSize}", price=DPPrice, qty=item_quantity)
                platter.save()
            except:
                messages.error(request, 'Please Submit a Valid Order!', fail_silently=True)
                return redirect("cart")

        # else loop as a layer of protection against the misuse of the HTML form
        else:
            raise Http404("OOPS!😥 WE COULDN'T FIND THE ITEM YOU WANTED TO ORDER")

    return redirect("cart")

@Authenticated_user
def checkOut(request):

    if request.method == "POST":

        payment = 0

        receipt_items = []
        
        objects = Cart.objects.filter(Q(customer=request.user))

        for price in Cart.objects.values_list('price', flat=True).filter(Q(customer=request.user)):
            payment += price

        # to display HST in the html file
        interest = (payment * Decimal(0.08))
        interest = Decimal("%.2f" % interest)

        # add the interest to the total price
        payment += interest

        # storing the items of the order in an array
        for item in objects:
            receipt_items.append(item)

        context = {
            'receipt': receipt_items,
            'payment': payment,
            'interest': interest,
        }

        return render(request, "orders/checkout.html", context)

    return redirect("cart")

@Authenticated_user
def removeItem(request):

    if request.method == "POST":

        item_id = request.POST["item_id"]
        try: 
            remove = Cart.objects.filter(Q(customer=request.user), Q(id=item_id)).delete()
            messages.success(request, "You have successfull removed the item from your cart", fail_silently=True)
        except:
            messages.error(request, "Unable to remove item", fail_silently=True)

    return redirect("cart")

@Authenticated_user
def completed(request):

    if request.method == 'POST':

        objects = Cart.objects.filter(Q(customer=request.user))
        
        order = Order(recipient=request.user)
        order.save()

        # creates a order for the customer
        for item in objects:
            order.items.add(item)
            order.save()
        
        # removes the items from the cart as they have been paid for 
        remove_items = objects.delete()

        # ordered items to show up on the console
        cart_items = json.loads(request.body)

        print("########################")
        print('customer:', request.user)
        print('payment_for:', cart_items)
        print("########################")

        return JsonResponse("Payment Successful", safe=False)

    return HttpResponse("Forbidden!")
