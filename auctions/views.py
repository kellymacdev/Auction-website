from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]





def index(request):
    all_listings = Listing.objects.all()
    listings_and_highest_bids = []
    for item in all_listings:
        highest_bid = item.bids.order_by("-bid_amount").first()
        listings_and_highest_bids.append({
            "listing": item,
            "highest_bid": highest_bid
        })
    return render(request, "auctions/index.html", {
            "listings_and_highest_bids": listings_and_highest_bids
            }) # returns list of all listings plus their highest bids

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
    item = Listing.objects.get(title=title)
    return render(request, "auctions/listing.html", {
        "item": item,
        "highest_bid": item.bids.order_by("-bid_amount").first()
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        new_listing = NewListingForm(request.POST)
        if new_listing.is_valid():
            title = new_listing.cleaned_data["title"]
            new= new_listing.save(commit=False)
            new.user = request.user
            new.save()
            return redirect(reverse("listing", args=[title]))
    else:
        return render(request, "auctions/create_listing.html", {
            "new_form": NewListingForm()
        })


@login_required
def new_bid(request,title):
    item = Listing.objects.get(title=title)
    if request.method == "POST":
        bid = int(request.POST.get("new_bid"))
        current_highest_bid = item.bids.order_by("-bid_amount").first()

        #if there has already been a bid
        if current_highest_bid is not None:
            current_bid_amount = int(current_highest_bid.bid_amount)
            if current_bid_amount >= bid: #new bid is less than highest bid
                return render(request, "auctions/listing.html", {
                    "item": item,
                    "equal_bid_message": True,
                    "highest_bid": item.bids.order_by("-bid_amount").first()
                })
            else:
                new_bid = Bid(bid_amount=bid, user=request.user, item=item)
                new_bid.save()
                return redirect('listing',title=item.title)

        #if there hasn't been a bid yet
        else:
            if item.starting_bid >= bid: #new bid is less than starting bid
                return render(request, "auctions/listing.html", {
                    "item": item,
                    "equal_bid_message": True
                    #f"You must bid higher than the starting bid of R{item.starting_bid}."
                })
            else:
                new_bid = Bid(bid_amount=bid, user=request.user, item=item)
                new_bid.save()
                return redirect('listing',title=item.title)




