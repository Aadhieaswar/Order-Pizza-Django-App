from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateUser
from django.contrib import messages

# Create your views here.
def index(request):

    if request.session.get("user") is not None:
        user = "Welcome " + request.session["user"] + "!"
    else:
        user = ""

    context = {
    'msg': user,
    }
    return render(request, "orders/index.html", context)

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

        elif user is None:
            messages.warning(request, 'Username and/or Password is incorrect')
            return render(request, "orders/login.html", context_instance=RequestContext)

    return render(request, "orders/login.html")

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

    context = {
    'title': 'Session end',
    'note': 'You have successfull been Logged Out!'
    }

    return render(request, "orders/message.html", context)
