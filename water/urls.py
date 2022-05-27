from django.urls import path
from . import views

urlpatterns = [

    path("home/", views.home,name="home"),
    path("usage/", views.usage, name="usage"),
    path("map/", views.map, name="map"),
    path("pricing/", views.pricing, name="pricing"),
    path("contact/", views.contact, name="contact"),

    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("registration/", views.registration, name="registration"),
    path("account/", views.account, name="account"),
]