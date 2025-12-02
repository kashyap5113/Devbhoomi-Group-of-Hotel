"""
Core App Models - Destinations and Contact Messages

File Location: core/models.py
"""

from django.db import models

class Destination(models.Model):
    """
    Popular destinations around Dwarka
    Examples: Dwarkadhish Temple, Gomti Ghat, Beyt Dwarka, etc.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="URL-friendly name")
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    distance_from_temple = models.CharField(
        max_length=100, 
        blank=True,
        help_text="e.g., '200m from Dwarkadhish Temple'"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on homepage"
    )
    highlight_points = models.TextField(
        blank=True,
        help_text="Optional bullet summary (one per line) for destination detail page"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"


class ContactMessage(models.Model):
    """
    Contact form submissions from users
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, help_text="Mark as read by admin")
    
    def __str__(self):
        return f"Message from {self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"


class DestinationImage(models.Model):
    destination = models.ForeignKey(
        Destination,
        related_name='gallery_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='destinations/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.destination.name} image #{self.order or self.id}"