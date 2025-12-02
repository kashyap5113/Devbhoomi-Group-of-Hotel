"""URL configuration for the bookings app."""

from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    # Booking form for a specific hotel selected via slug
    path("hotel/<slug:hotel_slug>/", views.booking_page, name="booking_page"),
    # Process booking submissions
    path("process/", views.process_booking, name="process"),
    # Razorpay verification callback
    path("verify-payment/", views.verify_razorpay_payment, name="verify_payment"),
    # Confirmation page showing booking summary
    path("confirmation/<str:booking_id>/", views.booking_confirmation, name="confirmation"),
    # Authenticated user's booking history
    path("my/", views.my_bookings, name="my_bookings"),
]