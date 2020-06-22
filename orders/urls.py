from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login_view", views.login_view, name="login_view"),
    path("signup_view", views.signup_view, name="signup_view"),
    path("login", views._login, name="_login"),
    path("logout", views._logout, name="_logout"),
    path("signup", views.signup, name="signup"),
]
