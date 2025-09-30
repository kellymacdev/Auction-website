from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #already has fields for username, email. password etc.
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image_url = models.URLField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"Listing {self.id}. {self.title}"

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass
