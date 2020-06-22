from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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
    return render(request, "orders/login.html")

def signup_view(request):
    return render(request, "orders/signup.html")

def _login(request):

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)

    if user is not None:
        name = user.username
        request.session["user"] = name

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "orders/login.html", {'msg': "Invalid Credentials!"})

def _logout(request):

    logout(request)
    request.session.clear()

    context = {
    'title': 'Session end',
    'message': 'You have successfull been Logged Out!'
    }

    return render(request, "orders/message.html", context)


def signup(request):

    return None
