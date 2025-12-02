"""Tests for bookings app"""

from django.test import TestCase, override_settings
from django.urls import reverse

from bookings.models import Payment
from hotels.models import Hotel, RoomType


class BookingPageViewTests(TestCase):
    """Verify booking page context information"""

    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            slug="test-hotel",
            description="Great stay",
            address="123 Temple Road",
            distance_from_temple="200m",
            base_price=3000,
        )
        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name="Deluxe",
            price_per_night=3500,
            capacity=2,
            max_guests=2,
            total_rooms=5,
        )

    @override_settings(RAZORPAY_KEY_ID="key123", RAZORPAY_KEY_SECRET="secret123")
    def test_booking_page_context_includes_razorpay_flag(self):
        url = reverse('bookings:booking_page', kwargs={'hotel_slug': self.hotel.slug})
        response = self.client.get(url, {'room': self.room_type.id})

        self.assertEqual(response.status_code, 200)
        self.assertIn('razorpay_enabled', response.context)
        self.assertTrue(response.context['razorpay_enabled'])


class PaymentModelTests(TestCase):
    """Ensure Payment configuration lists Razorpay option"""

    def test_contains_razorpay_method(self):
        methods = dict(Payment.PAYMENT_METHODS)
        self.assertIn('razorpay', methods)
