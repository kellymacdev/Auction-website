from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:item_id>", views.listing, name="listing"),
    path("listing/<int:item_id>/new_bid", views.new_bid, name="new_bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:item_id>/close_listing", views.close_listing, name="close_listing"),
    path("past_auctions", views.past_auctions, name="past_auctions"),
    path("listing/<int:item_id>/add_to_watchlist", views.add_watchlist, name="add_watchlist"),
path("listing/<int:item_id>/remove_from_watchlist", views.remove_watchlist, name="remove_watchlist"),
]
