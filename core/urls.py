"""URL configuration for the core app."""

from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    # Homepage
    path("", views.index, name="index"),
    # About Dwarka page
    path("about/", views.about_dwarka, name="about"),
    # Contact form page
    path("contact/", views.contact, name="contact"),
]