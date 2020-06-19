from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):

    context = {
    'msg': ""
    }
    return render(request, "orders/index.html", context)

# use request.session["var"] to set session variables
# user request.session.clear() to clear the session

def login(request):
    return render(request, "orders/login.html", context)

def signup(request):
    return render(request, "orders/signup.html", context)
