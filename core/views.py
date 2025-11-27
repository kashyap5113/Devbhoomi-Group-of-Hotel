"""
Core app views - Homepage and general pages
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Destination, ContactMessage
from hotels.models import Hotel

def index(request):
    """Homepage view"""
    featured_hotels = Hotel.objects.filter(is_featured=True)[:3]
    top_rated_hotels = Hotel.objects.filter(is_active=True).order_by('-rating')[:6]
    destinations = Destination.objects.filter(is_featured=True)[:4]
    
    context = {
        'featured_hotels': featured_hotels,
        'top_rated_hotels': top_rated_hotels,
        'destinations': destinations,
    }
    return render(request, 'home/index.html', context)


def about_dwarka(request):
    """About Dwarka page"""
    return render(request, 'home/about_dwarka.html')


def contact(request):
    """Contact page with form submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        
        messages.success(request, 'Thank you! Your message has been sent successfully.')
        return redirect('core:contact')
    
    return render(request, 'home/contact.html')

