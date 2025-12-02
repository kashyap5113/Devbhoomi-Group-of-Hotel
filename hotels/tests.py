from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Hotel, Review


class ReviewPermissionsTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.author = User.objects.create_user(username='author', password='pass123')
        self.other_user = User.objects.create_user(username='other', password='pass123')
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='pass123'
        )
        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            slug='test-hotel',
            description='Nice place',
            address='123 Main St',
            distance_from_temple='100m',
            base_price=2000,
        )
        self.review = Review.objects.create(
            hotel=self.hotel,
            guest_name='Author',
            rating=5,
            comment='Great stay',
            stay_date='2024-01-01',
            is_approved=True,
            author=self.author,
        )
        self.detail_url = reverse('hotels:details', args=[self.hotel.slug])

    def test_non_author_cannot_delete_review(self):
        self.client.login(username='other', password='pass123')
        response = self.client.post(self.detail_url, {'delete_review_id': self.review.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())

    def test_author_can_delete_review(self):
        self.client.login(username='author', password='pass123')
        response = self.client.post(self.detail_url, {'delete_review_id': self.review.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_admin_can_delete_review(self):
        self.client.login(username='admin', password='pass123')
        response = self.client.post(self.detail_url, {'delete_review_id': self.review.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())
