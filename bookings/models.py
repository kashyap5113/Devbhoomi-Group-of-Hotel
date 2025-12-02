"""
Bookings App Models - Booking, Guest Details, Payment, Coupons

File Location: bookings/models.py
"""

from django.db import models
from django.contrib.auth.models import User
from hotels.models import Hotel, RoomType
import uuid


class Booking(models.Model):
    """
    Main booking model - stores all booking information
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Unique Booking ID
    booking_id = models.CharField(
        max_length=20, 
        unique=True, 
        editable=False,
        help_text="Auto-generated unique booking ID"
    )
    
    # User (optional - can be guest booking)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Leave blank for guest bookings"
    )
    
    # Hotel & Room Information
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    
    # Booking Dates
    check_in = models.DateField()
    check_out = models.DateField()
    nights = models.IntegerField(help_text="Number of nights")
    
    # Guest Information
    num_adults = models.IntegerField(default=2)
    num_children = models.IntegerField(default=0)
    num_rooms = models.IntegerField(default=1)
    
    # Pricing Details
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Room price x nights x rooms"
    )
    discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text="Hotel discount amount"
    )
    taxes = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text="GST and other taxes"
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Final amount to be paid"
    )
    
    # Coupon Information
    coupon_code = models.CharField(max_length=50, blank=True)
    coupon_discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0
    )
    
    # Booking Status
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS, 
        default='pending'
    )
    
    # Special Requests
    special_requests = models.TextField(
        blank=True,
        help_text="Any special requirements from guest"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Generate unique booking ID"""
        if not self.booking_id:
            # Format: DWK + 8 random characters
            self.booking_id = f"DWK{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.booking_id} - {self.hotel.name}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"


class GuestDetail(models.Model):
    """
    Guest personal information for booking
    """
    
    ID_TYPES = [
        ('aadhaar', 'Aadhaar Card'),
        ('pan', 'PAN Card'),
        ('license', 'Driving License'),
        ('passport', 'Passport'),
    ]
    
    TITLE_CHOICES = [
        ('Mr', 'Mr.'),
        ('Mrs', 'Mrs.'),
        ('Ms', 'Ms.'),
    ]
    
    booking = models.OneToOneField(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='guest_detail'
    )
    
    # Personal Information
    title = models.CharField(max_length=5, choices=TITLE_CHOICES)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # ID Proof Information
    id_type = models.CharField(max_length=20, choices=ID_TYPES)
    id_number = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.full_name} - {self.booking.booking_id}"
    
    class Meta:
        verbose_name = "Guest Detail"
        verbose_name_plural = "Guest Details"


class Payment(models.Model):
    """
    Payment transaction details for booking
    """
    
    PAYMENT_METHODS = [
        ('card', 'Credit/Debit Card'),
        ('netbanking', 'Net Banking'),
        ('upi', 'UPI'),
        ('razorpay', 'Pay Online (Razorpay)'),
        ('payathotel', 'Pay at Hotel'),
    ]
    
    booking = models.OneToOneField(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='payment'
    )
    
    # Payment Information
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Payment gateway transaction ID"
    )
    gateway_order_id = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="Razorpay order identifier"
    )
    gateway_payment_id = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="Razorpay payment identifier"
    )
    gateway_signature = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text="Signature returned by Razorpay"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment Status
    is_successful = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Additional Information
    remarks = models.TextField(
        blank=True,
        help_text="Any payment-related notes"
    )
    
    def __str__(self):
        return f"Payment for {self.booking.booking_id}"
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class Coupon(models.Model):
    """
    Discount coupons for bookings
    """
    
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    code = models.CharField(
        max_length=50, 
        unique=True,
        help_text="Coupon code (e.g., FIRST500, TEMPLE20)"
    )
    description = models.CharField(
        max_length=200,
        help_text="User-friendly description"
    )
    
    # Discount Configuration
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPES,
        default='percentage'
    )
    discount_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Percentage (e.g., 20) or Fixed amount (e.g., 500)"
    )
    
    # Conditions
    min_booking_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text="Minimum booking amount to apply coupon"
    )
    max_discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Maximum discount amount (for percentage type)"
    )
    
    # Validity Period
    valid_from = models.DateField()
    valid_until = models.DateField()
    
    # Usage Limits
    max_uses = models.IntegerField(
        default=100,
        help_text="Maximum number of times this coupon can be used"
    )
    used_count = models.IntegerField(
        default=0,
        help_text="Number of times already used"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.code} - {self.description}"
    
    def is_valid(self):
        """Check if coupon is currently valid"""
        from django.utils import timezone
        today = timezone.now().date()
        return (
            self.is_active and 
            self.valid_from <= today <= self.valid_until and 
            self.used_count < self.max_uses
        )
    
    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
        ordering = ['-created_at'] if 'created_at' in locals() else ['code']