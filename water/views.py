from audioop import reverse
from unicodedata import name
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .data.datacalc import Environment
from .models import Searches


# from .models import User
messagess = []


def home(request):
    return render(
        request,
        "home.html",
        {
            "name": "home",
        },
    )


def usage(request):
    return render(request, "usage.html", {"name": "usage"})


def map(request):
    if request.method == "GET":
        context = {"name": "map"}
        return render(request, "map.html", context)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return render(request, "login.html", {"name": "login"})

        product = Searches.objects.get(user=request.user)
        if product.avsearches == 0:
            return render(request, "pricing.html", {"name": "pricing"})

        else:
            try:
                results = request.POST["coords"].split(",")
                lat, lng = float(results[0][10:]), float(results[1][9:-1])
                crop = request.POST["crop"]

                env_info = Environment(crop.upper(), (lat, lng))
                env_info.get_water_req()
                water_req = env_info.parse_to_json()

                context = water_req
                page = "results.html"

                # the part to -1 search
                product = Searches.objects.get(user=request.user)
                product.avsearches = product.avsearches - 1
                product.save()
                return render(request, page, context)

            except:
                context = {}
                page = "results_error.html"
                return render(request, page, context)


def pricing(request):
    return render(request, "pricing.html", {"name": "pricing"})


def contact(request):
    if request.method == "GET":
        return render(request, "contact.html", {"name": "contact"})

    if request.method == "POST":
        global messagess
        messagess.append(request.POST)
        print(messagess)
        return render(
            request,
            "contact.html",
            {"name": "contact", "message": "Your message has been sent. Thank you!"},
        )


def login(request):
    if request.method == "GET":
        return render(request, "login.html", {"name": "login"})

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, "map.html", {"name": "map"})
        else:
            return render(request, "login.html", {"message": "Invalid Credentials"})


def logout(request):
    auth_logout(request)
    return render(request, "home.html", {"name": "home"})


def registration(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)

            addtostart = Searches(user=request.user, avsearches=5)
            addtostart.save()
            return redirect("map")
    else:
        form = SignUpForm()
    return render(request, "registration.html", {"form": form})


def account(request):
    if not request.user.is_authenticated:
        return render(request, "login.html", {"name": "login"})
    else:
        avsearches = Searches.objects.get(user=request.user)
        return render(
            request, "account.html", {"name": "account", "avsearches": avsearches}
        )
