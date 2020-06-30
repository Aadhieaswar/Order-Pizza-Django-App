from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateUser
from .decorators import Unauthenticated_user
from .models import *

# Create your views here.

Menu = {
'pizza': Pizza.objects.all(),
'salad': Salad.objects.all(),
'sub': Sub.objects.all(),
'dinnerplatter': DinnerPlatter.objects.all(),
'pasta': Pasta.objects.all(),
'topping': Topping.objects.all(),
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
            print("fking cookies")
            return render(request, "orders/login.html")

    return render(request, "orders/login.html")

@Unauthenticated_user
def signup_view(request):

    form = CreateUser()

    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {
    'form': form,
    }

    return render(request, "orders/signup.html", context)

def _logout(request):

    logout(request)
    request.session.clear()

    return redirect("home")
