"""
Users App Models - Extended User Profile

File Location: users/models.py
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extended user profile with additional information
    Automatically created when a user registers
    """
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    # Contact Information
    phone = models.CharField(
        max_length=20, 
        blank=True,
        help_text="Primary contact number"
    )
    alternate_phone = models.CharField(
        max_length=20, 
        blank=True,
        help_text="Alternate contact number"
    )
    
    # Personal Information
    date_of_birth = models.DateField(
        null=True, 
        blank=True
    )
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        blank=True
    )
    
    # Address Information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    country = models.CharField(
        max_length=100, 
        default='India',
        blank=True
    )
    
    # Profile Picture
    profile_picture = models.ImageField(
        upload_to='profiles/', 
        blank=True, 
        null=True
    )
    
    # Preferences
    receive_email_notifications = models.BooleanField(
        default=True,
        help_text="Receive booking confirmations and offers via email"
    )
    receive_sms_notifications = models.BooleanField(
        default=True,
        help_text="Receive booking updates via SMS"
    )

    # Two-Factor Authentication (TOTP)
    otp_secret = models.CharField(
        max_length=32,
        blank=True,
        help_text="Base32 secret for authenticator apps",
    )
    otp_enabled = models.BooleanField(
        default=False,
        help_text="Require OTP verification for master module",
    )
    otp_last_verified = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create UserProfile when a User is created
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save UserProfile whenever User is saved
    """
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)