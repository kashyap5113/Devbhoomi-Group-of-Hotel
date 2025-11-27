"""URL configuration for the hotels app."""

from django.urls import path

from . import views

app_name = "hotels"

urlpatterns = [
    # Search listing for hotels with filters
    path("", views.search_hotels, name="search"),
    # Individual hotel details page using slug in the URL
    path("<slug:slug>/", views.hotel_details, name="details"),
]