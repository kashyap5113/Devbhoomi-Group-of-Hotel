"""
Users app views - Login, Signup, Profile
"""

import pyotp

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from bookings.models import Booking
from .forms import LoginForm, OTPVerificationForm, SignupForm
from .models import UserProfile

def user_login(request):
    """User login view"""
    form = LoginForm(request.POST or None)

    # Clear any stale success/error notices (e.g., from logout/booking) when simply visiting the page
    if request.method != 'POST':
        list(messages.get_messages(request))

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            request.session['post_auth_next'] = request.GET.get('next', 'core:index')
            request.session['post_auth_user_id'] = user.id
            if hasattr(user, 'profile') and user.profile.otp_enabled:
                return redirect('users:otp-verify')
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect(request.session.pop('post_auth_next', 'core:index'))
        else:
            messages.error(request, 'Please fix the errors below to continue.')

    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


@login_required
def otp_setup(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if not profile.otp_secret:
        profile.otp_secret = pyotp.random_base32()
        profile.save()

    otp_uri = pyotp.totp.TOTP(profile.otp_secret).provisioning_uri(
        name=request.user.email or request.user.username,
        issuer_name="Dwarka Getaways"
    )

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            totp = pyotp.TOTP(profile.otp_secret)
            if totp.verify(form.cleaned_data['token']):
                profile.otp_enabled = True
                profile.otp_last_verified = timezone.now()
                profile.save()
                messages.success(request, 'Two-factor authentication enabled!')
                return redirect('users:dashboard')
            messages.error(request, 'Invalid code. Try again.')
    else:
        form = OTPVerificationForm()

    return render(
        request,
        'users/otp_setup.html',
        {
            'profile': profile,
            'otp_uri': otp_uri,
            'form': form,
        },
    )


def otp_verify(request):
    user_id = request.session.get('post_auth_user_id')
    if not user_id:
        return redirect('users:login')

    user = User.objects.filter(id=user_id).first()
    if not user or not hasattr(user, 'profile') or not user.profile.otp_enabled:
        return redirect('users:login')

    form = OTPVerificationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        totp = pyotp.TOTP(user.profile.otp_secret)
        if totp.verify(form.cleaned_data['token']):
            login(request, user)
            user.profile.otp_last_verified = timezone.now()
            user.profile.save()
            request.session.pop('post_auth_user_id', None)
            messages.success(request, 'OTP verified successfully.')
            return redirect(request.session.pop('post_auth_next', 'core:index'))
        messages.error(request, 'Invalid code. Please try again.')

    return render(request, 'users/otp_verify.html', {'form': form})


def user_signup(request):
    """User signup view"""
    form = SignupForm(request.POST or None)

    # Ensure stale messages from previous flows don't clutter the signup view
    if request.method != 'POST':
        list(messages.get_messages(request))

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
