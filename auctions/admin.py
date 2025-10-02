from django.contrib import admin
from django.utils.html import format_html

from .models import User, Listing, Bid, Comment, Watchlist

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title","user","active", "starting_bid","highest_bid", "winning_bid")

    def winning_bid(self,obj):
        if obj.active is False:
            if obj.winner:
                win_bid = obj.bids.order_by("-bid_amount").first()
                return f"{obj.winner} with R{win_bid.bid_amount} bid"
            else:
                return "Closed with no bids"
        else:
            return ""
    winning_bid.short_description = "Winner"

    def highest_bid(self,obj):
        highest = obj.bids.order_by("-bid_amount").first()
        if highest:
            return f"{highest.user.username}: {highest.bid_amount}"
        return "No bids"
    highest_bid.short_description = "Highest bid"

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "user_listings", "user_bids", "user_comments", "user_watchlist")

    def user_bids(self, obj):
        vertical_bids = [f"{bid.item.title}: {bid.bid_amount}" for bid in obj.bids.all()]
        return format_html("<br>".join(vertical_bids))
    user_bids.short_description = "Bids"

    def user_comments(self, obj):
        vertical_comments = [f"Comment on {comment.listing.title} saying '{comment.comment}'" for comment in obj.comments.all()]
        return format_html("<br>".join(vertical_comments))
    user_comments.short_description = "Comments"

    def user_listings(self, obj):
        vertical_listings = [listing.title for listing in obj.listings.all()]
        return format_html("<br>".join(vertical_listings))
    user_listings.short_description = "Listings"

    def user_watchlist(self, obj):
        vertical_watchlist = [item.listing.title for item in obj.watchlist.all()]
        return format_html("<br>".join(vertical_watchlist))
    user_watchlist.short_description = "Watchlist"


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)