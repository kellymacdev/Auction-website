from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Listing

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]





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

@login_required
def create_listing(request):
    if request.method == "POST":
        new_listing = NewListingForm(request.POST)
        if new_listing.is_valid():
            title = new_listing.cleaned_data["title"]
            new_listing.save()
            return redirect(reverse("listing", args=[title]))
    else:
        return render(request, "auctions/create_listing.html", {
            "new_form": NewListingForm()
        })


@login_required
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
