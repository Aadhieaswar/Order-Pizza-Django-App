from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def index(request):

    context = {
    'msg': ""
    }
    return render(request, "orders/index.html", context)

# use request.session["var"] = value --> to set session variables
# user request.session.clear() --> to clear the session

def login(request):
    return render(request, "orders/login.html")

def signup(request):
    return render(request, "orders/signup.html")
