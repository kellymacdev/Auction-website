from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Watchlist


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]





def index(request):
    active_listings = Listing.objects.filter(active=True)
    listings_and_highest_bids = []
    for item in active_listings:
        highest_bid = item.bids.order_by("-bid_amount").first()
        listings_and_highest_bids.append({
            "listing": item,
            "highest_bid": highest_bid
        })
    return render(request, "auctions/index.html", {
            "listings_and_highest_bids": listings_and_highest_bids
            }) # returns list of all listings plus their highest bids


def past_auctions(request):
    closed_listings = Listing.objects.filter(active=False)
    closed_listings_and_highest_bids = []
    for item in closed_listings:
        highest_bid = item.bids.order_by("-bid_amount").first()
        closed_listings_and_highest_bids.append({
            "listing": item,
            "highest_bid": highest_bid
        })
    return render(request, "auctions/past_auctions.html",{
        "closed_listings": closed_listings_and_highest_bids
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

def listing(request, item_id):
    item = Listing.objects.get(pk=item_id)
    in_watchlist = Watchlist.objects.filter(user=request.user, listing=item).exists()
    return render(request, "auctions/listing.html", {
        "item": item,
        "highest_bid": item.bids.order_by("-bid_amount").first(),
        "in_watchlist": in_watchlist
    })

def categories(request):
    #get a list of the categories from all active listings (flat = True just gives straight list rather than tuples)
    #and excludes all the empty categories
    active_listing_categories = Listing.objects.filter(active=True).exclude(category='').values_list("category", flat=True)
    return render(request, "auctions/categories.html", {
        "active_categories": active_listing_categories
    })

def category(request, cat):
    listings_in_cat = Listing.objects.filter(active=True, category=cat)
    return render(request, "auctions/category.html",{
        "listings_in_category": listings_in_cat,
        "category_name": cat
    })


@login_required
def create_listing(request):
    if request.method == "POST":
        new_listing = NewListingForm(request.POST)
        if new_listing.is_valid():
            new= new_listing.save(commit=False)
            new.user = request.user
            new.save()
            return redirect("listing", item_id=new.id)
    else:
        return render(request, "auctions/create_listing.html", {
            "new_form": NewListingForm()
        })


@login_required
def new_bid(request,item_id):
    item = Listing.objects.get(pk=item_id)
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
                new_bid1 = Bid(bid_amount=bid, user=request.user, item=item)
                new_bid1.save()
                return redirect('listing',item_id=item.id)

        #if there hasn't been a bid yet
        else:
            if item.starting_bid >= bid: #new bid is less than starting bid
                return render(request, "auctions/listing.html", {
                    "item": item,
                    "equal_bid_message": True
                })
            else:
                new_bid2 = Bid(bid_amount=bid, user=request.user, item=item)
                new_bid2.save()
                return redirect('listing',item_id=item.id)


@login_required
def watchlist(request):
    users_watchlist1 = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": users_watchlist1
    })

@login_required
def close_listing(request, item_id):
    if request.method == "POST":
        item = Listing.objects.get(pk=item_id)
        item.active = False
        if item.bids:
            item.winner = item.bids.order_by("-bid_amount").first().user
        item.save()

        return redirect("listing", item_id=item.id)


@login_required
def add_watchlist(request, item_id):
    if request.method == "POST":
        item = Listing.objects.get(pk=item_id)
        new_entry = Watchlist(user=request.user, listing=item)
        new_entry.save()
        return redirect("listing", item_id=item.id)

@login_required
def remove_watchlist(request, item_id):
    if request.method == "POST":
        item = Listing.objects.get(pk=item_id)
        Watchlist.objects.filter(user=request.user, listing=item).delete()
        return redirect("listing", item_id=item.id)


 #