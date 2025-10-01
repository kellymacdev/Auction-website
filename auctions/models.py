from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #already has fields for username, email. password etc.
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    current_bid = models.IntegerField(default=0, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, related_name='won_listing', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Listing {self.id}. {self.title}"

class Bid(models.Model):
    bid_amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    #to link a user to their bids. On deleting a user, their bids are deleted too
    #to link an item to bids. "

    def __str__(self):
        return f"{self.user} bid R{self.bid_amount} on {self.item} listing"

class Comment(models.Model):
    pass

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(Listing, related_name='watchers', on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'listing'], name='unique_watchlist')]

    def __str__(self):
        return f"{self.user}'s watchlist includes {self.listing}"