"""
Core App Admin Configuration

File Location: core/admin.py
"""

from django.contrib import admin

from .models import ContactMessage, Destination, DestinationImage


class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1
    fields = ["image", "caption", "order"]
    ordering = ["order"]


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    """Admin interface for Destinations"""
    
    list_display = [
        'name', 
        'distance_from_temple', 
        'is_featured', 
        'created_at'
    ]
    
    list_filter = [
        'is_featured', 
        'created_at'
    ]
    
    search_fields = [
        'name', 
        'description'
    ]
    
    prepopulated_fields = {
        'slug': ('name',)
    }
    
    list_editable = ['is_featured']
    inlines = [DestinationImageInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for Contact Messages"""
    
    list_display = [
        'name', 
        'email', 
        'phone', 
        'created_at', 
        'is_read'
    ]
    
    list_filter = [
        'is_read', 
        'created_at'
    ]
    
    search_fields = [
        'name', 
        'email', 
        'message'
    ]
    
    readonly_fields = [
        'name', 
        'email', 
        'phone', 
        'message', 
        'created_at'
    ]
    
    list_editable = ['is_read']
    
    date_hierarchy = 'created_at'