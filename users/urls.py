"""URL configuration for the users app."""

from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    # Authentication views
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    # Dashboard for logged-in users (includes profile editing)
    path("dashboard/", views.user_dashboard, name="dashboard"),
]