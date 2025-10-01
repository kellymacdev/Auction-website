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
    current_bid = models.IntegerField(default=0)

    def __str__(self):
        return f"Listing {self.id}. {self.title}"

class Bid(models.Model):
    pass
    #bid_amount = models.IntegerField(default=0)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #to link a user to a bid, on deleting a user, their bids are deleted too

class Comment(models.Model):
    pass
