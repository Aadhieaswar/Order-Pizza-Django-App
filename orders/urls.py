from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login_view/", views.login_view, name="login_view"),
    path("signup_view/", views.signup_view, name="signup_view"),
    path("logout/", views._logout, name="_logout"),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/", views.submit_order, name="submit_order"),
    path("check_out/", views.checkOut, name="check_out"),
    path("remove_item/", views.removeItem, name="remove_item"),
    path("checkout/", views.sample, name="check")
]
