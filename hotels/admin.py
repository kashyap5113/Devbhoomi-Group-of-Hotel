"""
Hotels App Admin Configuration

File Location: hotels/admin.py
"""

from django.contrib import admin
from .models import Hotel, HotelImage, RoomType, Amenity, Review


class HotelImageInline(admin.TabularInline):
    """Inline admin for hotel images"""
    model = HotelImage
    extra = 3
    fields = ['image', 'caption', 'order']


class RoomTypeInline(admin.TabularInline):
    """Inline admin for room types"""
    model = RoomType
    extra = 2
    fields = ['name', 'max_guests', 'price_per_night', 'total_rooms', 'is_available']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """Admin interface for Hotels"""
    
    list_display = [
        'name', 
        'property_type', 
        'star_rating', 
        'rating', 
        'base_price', 
        'discount_percentage', 
        'is_featured', 
        'is_active'
    ]
    
    list_filter = [
        'property_type', 
        'star_rating', 
        'is_featured', 
        'is_active',
        'created_at'
    ]
    
    search_fields = [
        'name', 
        'address', 
        'description',
        'distance_from_temple'
    ]
    
    prepopulated_fields = {
        'slug': ('name',)
    }
    
    filter_horizontal = ['amenities']
    
    list_editable = [
        'is_featured', 
        'is_active'
    ]
    
    inlines = [HotelImageInline, RoomTypeInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 
                'slug', 
                'property_type', 
                'description', 
                'main_image'
            )
        }),
        ('Location', {
            'fields': (
                'address', 
                'distance_from_temple', 
                'landmark'
            )
        }),
        ('Pricing', {
            'fields': (
                'base_price', 
                'discount_percentage'
            )
        }),
        ('Ratings & Reviews', {
            'fields': (
                'star_rating', 
                'rating', 
                'total_reviews'
            )
        }),
        ('Features & Amenities', {
            'fields': (
                'amenities',
                'has_temple_view',
                'has_free_cancellation',
                'has_breakfast',
                'has_parking',
                'has_wifi',
                'has_ac'
            )
        }),
        ('Status & Display', {
            'fields': (
                'is_active',
                'is_featured',
                'badge'
            )
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    """Admin interface for Amenities"""
    
    list_display = ['name', 'icon']
    search_fields = ['name']
    ordering = ['name']


@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    """Admin interface for Hotel Images"""
    
    list_display = ['hotel', 'caption', 'order']
    list_filter = ['hotel']
    search_fields = ['hotel__name', 'caption']
    ordering = ['hotel', 'order']


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    """Admin interface for Room Types"""
    
    list_display = [
        'hotel', 
        'name', 
        'max_guests', 
        'price_per_night', 
        'total_rooms',
        'is_available'
    ]
    
    list_filter = [
        'hotel', 
        'is_available'
    ]
    
    search_fields = [
        'name', 
        'hotel__name'
    ]
    
    list_editable = ['is_available']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for Reviews"""
    
    list_display = [
        'guest_name', 
        'hotel', 
        'rating', 
        'stay_date', 
        'created_at',
        'is_approved'
    ]
    
    list_filter = [
        'is_approved', 
        'rating', 
        'created_at',
        'hotel'
    ]
    
    search_fields = [
        'guest_name', 
        'hotel__name', 
        'comment'
    ]
    
    list_editable = ['is_approved']
    
    readonly_fields = ['created_at']
    
    actions = ['approve_reviews', 'unapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        """Approve selected reviews"""
        updated = queryset.update(is_approved=True)
        self.message_user(
            request, 
            f'{updated} review(s) approved successfully.'
        )
    approve_reviews.short_description = "Approve selected reviews"
    
    def unapprove_reviews(self, request, queryset):
        """Unapprove selected reviews"""
        updated = queryset.update(is_approved=False)
        self.message_user(
            request, 
            f'{updated} review(s) unapproved.'
        )
    unapprove_reviews.short_description = "Unapprove selected reviews"  