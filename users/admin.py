"""
Users App Admin Configuration

File Location: users/admin.py
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline admin for user profile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = [
        'phone',
        'alternate_phone',
        'date_of_birth',
        'gender',
        'address',
        'city',
        'state',
        'pincode',
        'country',
        'profile_picture',
        'receive_email_notifications',
        'receive_sms_notifications'
    ]


class UserAdmin(BaseUserAdmin):
    """Extended User admin with profile information"""
    inlines = [UserProfileInline]
    
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'get_phone',
        'is_staff',
        'is_active',
        'date_joined'
    ]
    
    list_filter = [
        'is_staff',
        'is_active',
        'date_joined'
    ]
    
    search_fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'profile__phone'
    ]
    
    def get_phone(self, obj):
        """Display phone number from profile"""
        try:
            return obj.profile.phone
        except:
            return "N/A"
    get_phone.short_description = "Phone"


# Unregister the default User admin
admin.site.unregister(User)

# Register the extended User admin
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for User Profiles"""
    
    list_display = [
        'user',
        'phone',
        'city',
        'state',
        'created_at'
    ]
    
    list_filter = [
        'state',
        'city',
        'gender',
        'receive_email_notifications',
        'receive_sms_notifications'
    ]
    
    search_fields = [
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name',
        'phone',
        'city',
        'state'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': (
                'phone',
                'alternate_phone'
            )
        }),
        ('Personal Information', {
            'fields': (
                'date_of_birth',
                'gender',
                'profile_picture'
            )
        }),
        ('Address', {
            'fields': (
                'address',
                'city',
                'state',
                'pincode',
                'country'
            )
        }),
        ('Preferences', {
            'fields': (
                'receive_email_notifications',
                'receive_sms_notifications'
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at'
            )
        }),
    )