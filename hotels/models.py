"""
Hotels App Models - Hotel, Amenities, Room Types, Reviews

File Location: hotels/models.py
"""

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


class Amenity(models.Model):
    """Hotel amenities like Wi-Fi, Pool, Parking, etc."""

    CATEGORY_CHOICES = [
        ("room", "Room"),
        ("food", "Food & Dining"),
        ("facility", "Facility"),
    ]

    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=50,
        help_text="Icon class (Bootstrap Icons, e.g., bi-wifi)",
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="room",
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ['name']


class Hotel(models.Model):
    """Main Hotel model with all details used across public + master modules."""

    PROPERTY_TYPES = [
        ('hotel', 'Hotel'),
        ('resort', 'Resort'),
        ('guesthouse', 'Guest House'),
        ('homestay', 'Homestay'),
    ]

    LOCATION_ZONES = [
        ('dwarkadhish', 'Dwarkadhish Temple'),
        ('gomti_ghat', 'Gomti Ghat'),
        ('dwarka_beach', 'Dwarka Beach'),
        ('bet_dwarka', 'Bet Dwarka'),
        ('other', 'Dwarka City (Other)'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    city = models.CharField(max_length=120, default="Dwarka")
    property_type = models.CharField(
        max_length=20, 
        choices=PROPERTY_TYPES, 
        default='hotel'
    )
    description = models.TextField()
    
    # Location
    address = models.TextField()
    distance_from_temple = models.CharField(
        max_length=100, 
        help_text="e.g., 200m from Dwarkadhish Temple"
    )
    landmark = models.CharField(max_length=200, blank=True)
    location_zone = models.CharField(
        max_length=40,
        choices=LOCATION_ZONES,
        default='dwarkadhish',
        help_text="Primary Dwarka landmark this hotel is closest to"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Optional latitude for map integrations",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Optional longitude for map integrations",
    )
    
    # Pricing
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Base price per night"
    )
    discount_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Discount percentage (0-100)"
    )
    
    # Ratings & Reviews
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
        help_text="Average rating (0-5)"
    )
    star_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        help_text="Star category (1-5 stars)"
    )
    total_reviews = models.IntegerField(default=0)
    
    # Features & Amenities
    amenities = models.ManyToManyField(Amenity, blank=True)
    has_temple_view = models.BooleanField(default=False)
    has_free_cancellation = models.BooleanField(default=True)
    has_breakfast = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)
    
    # Status & Featured
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="Show in featured section on homepage"
    )
    badge = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g., Best Rated, Top Pick, Premium, New"
    )
    
    # Images
    main_image = models.FileField(
        upload_to='hotels/main/', 
        blank=True, 
        null=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from name"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def discounted_price(self):
        """Calculate price after discount"""
        if self.discount_percentage > 0:
            discount_amount = (self.base_price * self.discount_percentage) / 100
            return self.base_price - discount_amount
        return self.base_price
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-is_featured', '-rating']


class HotelImage(models.Model):
    """
    Additional images for hotel gallery
    """
    hotel = models.ForeignKey(
        Hotel, 
        related_name='images', 
        on_delete=models.CASCADE
    )
    image = models.FileField(upload_to='hotels/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0, help_text="Display order")
    
    def __str__(self):
        return f"{self.hotel.name} - Image {self.order}"
    
    class Meta:
        ordering = ['order']


class RoomType(models.Model):
    """Different room types available in a hotel"""

    BED_CHOICES = [
        ("single", "Single"),
        ("double", "Double"),
        ("twin", "Twin"),
        ("suite", "Suite"),
    ]

    hotel = models.ForeignKey(
        Hotel,
        related_name='room_types',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100,
        help_text="e.g., Deluxe Room, Suite, Standard Room"
    )
    slug = models.SlugField(max_length=140, blank=True)
    description = models.TextField(blank=True)
    bed_type = models.CharField(max_length=20, choices=BED_CHOICES, default="double")
    capacity = models.PositiveIntegerField(default=2, help_text="Total guests allowed")
    max_guests = models.IntegerField(default=2)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    size_sqft = models.PositiveIntegerField(default=250)
    total_rooms = models.IntegerField(default=1, help_text="Total rooms available")
    amenities = models.ManyToManyField(Amenity, blank=True)
    image = models.ImageField(upload_to='hotels/rooms/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.hotel.slug}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"

    class Meta:
        ordering = ['price_per_night']


class Review(models.Model):
    """
    Guest reviews for hotels
    """
    hotel = models.ForeignKey(
        Hotel, 
        related_name='reviews', 
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='hotel_reviews',
        help_text="Authenticated user who left the review (optional)"
    )
    guest_name = models.CharField(max_length=200)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating 1-5 stars"
    )
    comment = models.TextField()
    stay_date = models.DateField(help_text="When did the guest stay")
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(
        default=False,
        help_text="Approve review to show on website"
    )
    
    def __str__(self):
        return f"{self.guest_name} - {self.hotel.name} ({self.rating}★)"
    
    class Meta:
        ordering = ['-created_at']