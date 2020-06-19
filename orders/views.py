from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    request.session["user"] = "name"
    request.session.clear()
    try:
        var = requet.session["username"]
    except:
        var = "session cleared"
    context = {
    'msg': var
    }
    return render(request, "orders/index.html", context)

def login(request):
    return render(request, "orders/login.html", context)

def signup(request):
    return render(request, "orders/signup.html", context)
