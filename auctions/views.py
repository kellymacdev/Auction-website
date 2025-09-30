from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing


def index(request):
    all_listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "active_listings": all_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, title):
    return render(request, "auctions/listing.html", {
        "item": Listing.objects.get(title=title),
    })

def create_listing(request):
    if request.method == "POST":
        title = request.POST["item_title"]
        description = request.POST["item_description"]
        starting_bid = request.POST["item_starting_bid"]
        image_url = request.POST["item_image_url"]
        category = request.POST["category"]
        new_listing = Listing(title=title, description=description, starting_bid=starting_bid,image_url=image_url,category=category)
        new_listing.save()
        return redirect(reverse("listing", args=[title]))
    else:
        return render(request, "auctions/create_listing.html")


def new_bid(request,title):
    item = Listing.objects.get(title=title)
    if request.method == "POST":
        bid = int(request.POST["new_bid"])

        if bid <= item.current_bid:
            return render(request, "auctions/listing.html", {
                "item": item,
                "bid_message": f"You must bid higher than item.current_bid."
            })
        else:
            item.current_bid = bid
            item.save()
            return render(request, "auctions/listing.html", {
            "item": Listing.objects.get(title=title)
            })
