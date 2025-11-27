"""
Users app views - Login, Signup, Profile
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import UserProfile
from .forms import LoginForm, SignupForm
from bookings.models import Booking

def user_login(request):
    """User login view"""
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'core:index')
            return redirect(next_url)
        else:
            messages.error(request, 'Please fix the errors below to continue.')

    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


def user_signup(request):
    """User signup view"""
    form = SignupForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please login to continue.')
            return redirect('users:login')
        else:
            messages.error(request, 'Please correct the highlighted errors.')

    context = {
        'form': form,
    }
    return render(request, 'users/signup.html', context)


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('core:index')


@login_required
def user_dashboard(request):
    """User dashboard view with bookings and profile editing"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Handle profile update
    if request.method == 'POST':
        # Validate phone number
        phone = request.POST.get('phone', '').strip()
        if phone:
            # Remove any non-numeric characters
            phone = ''.join(filter(str.isdigit, phone))
            # Validate length
            if len(phone) != 10:
                messages.error(request, 'Phone number must be exactly 10 digits.')
                # Get bookings for context
                all_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
                today = timezone.now().date()
                upcoming_bookings = all_bookings.filter(check_in__gte=today, status__in=['pending', 'confirmed'])
                previous_bookings = all_bookings.filter(
                    Q(check_out__lt=today) | Q(status__in=['completed', 'cancelled'])
                )
                context = {
                    'profile': profile,
                    'upcoming_bookings': upcoming_bookings,
                    'previous_bookings': previous_bookings,
                    'total_bookings': all_bookings.count(),
                }
                return render(request, 'users/dashboard.html', context)
        
        # Update user info
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Update profile
        profile.phone = phone
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.pincode = request.POST.get('pincode', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:dashboard')
    
    # Get all bookings for the user
    all_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    # Separate upcoming and previous bookings
    today = timezone.now().date()
    upcoming_bookings = all_bookings.filter(check_in__gte=today, status__in=['pending', 'confirmed'])
    previous_bookings = all_bookings.filter(
        Q(check_out__lt=today) | Q(status__in=['completed', 'cancelled'])
    )
    
    context = {
        'profile': profile,
        'upcoming_bookings': upcoming_bookings,
        'previous_bookings': previous_bookings,
        'total_bookings': all_bookings.count(),
    }
    
    return render(request, 'users/dashboard.html', context)
