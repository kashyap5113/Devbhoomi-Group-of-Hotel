"""
Bookings App Admin Configuration

File Location: bookings/admin.py
"""

from django.contrib import admin
from .models import Booking, GuestDetail, Payment, Coupon


class GuestDetailInline(admin.StackedInline):
    """Inline admin for guest details"""
    model = GuestDetail
    extra = 0
    fields = [
        'title', 
        'full_name', 
        'email', 
        'phone', 
        'id_type', 
        'id_number'
    ]


class PaymentInline(admin.StackedInline):
    """Inline admin for payment details"""
    model = Payment
    extra = 0
    fields = [
        'payment_method', 
        'transaction_id', 
        'amount', 
        'is_successful', 
        'payment_date', 
        'remarks'
    ]
    readonly_fields = ['payment_date']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin interface for Bookings"""
    
    list_display = [
        'booking_id', 
        'hotel', 
        'guest_name', 
        'check_in', 
        'check_out',
        'nights',
        'total_amount', 
        'status', 
        'payment_status', 
        'created_at'
    ]
    
    list_filter = [
        'status', 
        'payment_status', 
        'check_in', 
        'created_at',
        'hotel'
    ]
    
    search_fields = [
        'booking_id', 
        'hotel__name', 
        'guest_detail__full_name',
        'guest_detail__email',
        'guest_detail__phone'
    ]
    
    readonly_fields = [
        'booking_id', 
        'created_at', 
        'updated_at'
    ]
    
    list_editable = [
        'status', 
        'payment_status'
    ]
    
    inlines = [GuestDetailInline, PaymentInline]
    
    date_hierarchy = 'check_in'
    
    fieldsets = (
        ('Booking Information', {
            'fields': (
                'booking_id',
                'user',
                'hotel',
                'room_type',
                'status',
                'payment_status'
            )
        }),
        ('Dates & Guests', {
            'fields': (
                'check_in',
                'check_out',
                'nights',
                'num_adults',
                'num_children',
                'num_rooms'
            )
        }),
        ('Pricing', {
            'fields': (
                'base_price',
                'discount_amount',
                'taxes',
                'coupon_code',
                'coupon_discount',
                'total_amount'
            )
        }),
        ('Additional Information', {
            'fields': (
                'special_requests',
                'created_at',
                'updated_at'
            )
        }),
    )
    
    def guest_name(self, obj):
        """Display guest name in list"""
        try:
            return obj.guest_detail.full_name
        except:
            return "N/A"
    guest_name.short_description = "Guest Name"
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_confirmed(self, request, queryset):
        """Mark selected bookings as confirmed"""
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} booking(s) marked as confirmed.')
    mark_as_confirmed.short_description = "Mark as Confirmed"
    
    def mark_as_completed(self, request, queryset):
        """Mark selected bookings as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} booking(s) marked as completed.')
    mark_as_completed.short_description = "Mark as Completed"
    
    def mark_as_cancelled(self, request, queryset):
        """Mark selected bookings as cancelled"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} booking(s) marked as cancelled.')
    mark_as_cancelled.short_description = "Mark as Cancelled"


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Admin interface for Coupons"""
    
    list_display = [
        'code', 
        'description',
        'discount_type', 
        'discount_value', 
        'valid_from', 
        'valid_until', 
        'used_count',
        'max_uses', 
        'is_active'
    ]
    
    list_filter = [
        'discount_type', 
        'is_active', 
        'valid_from', 
        'valid_until'
    ]
    
    search_fields = [
        'code', 
        'description'
    ]
    
    list_editable = ['is_active']
    
    fieldsets = (
        ('Coupon Information', {
            'fields': (
                'code',
                'description',
                'is_active'
            )
        }),
        ('Discount Configuration', {
            'fields': (
                'discount_type',
                'discount_value',
                'min_booking_amount',
                'max_discount'
            )
        }),
        ('Validity', {
            'fields': (
                'valid_from',
                'valid_until'
            )
        }),
        ('Usage', {
            'fields': (
                'max_uses',
                'used_count'
            )
        }),
    )
    
    readonly_fields = ['used_count']