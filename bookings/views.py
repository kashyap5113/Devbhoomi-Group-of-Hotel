"""
Bookings app views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
from .models import Booking, GuestDetail, Payment, Coupon
from hotels.models import Hotel, RoomType

def booking_page(request, hotel_slug, room_type_id=None):
    """Booking page for a specific hotel"""
    hotel = get_object_or_404(Hotel, slug=hotel_slug, is_active=True)

    # Determine selected room type
    room_queryset = hotel.room_types.filter(is_available=True)
    room_type = None
    if room_type_id:
        room_type = get_object_or_404(room_queryset, id=room_type_id)
    else:
        room_type_param = request.GET.get('room')
        if room_type_param:
            room_type = room_queryset.filter(id=room_type_param).first()
    room_type = room_type or room_queryset.first()

    # Get search parameters from session or query params
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    adults = int(request.GET.get('adults', 2))
    children = int(request.GET.get('children', 0))
    rooms = int(request.GET.get('rooms', 1))

    # Calculate nights
    nights = 0
    checkin_date = checkout_date = None
    if checkin and checkout:
        try:
            checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()
            nights = max((checkout_date - checkin_date).days, 1)
        except ValueError:
            checkin_date = checkout_date = None

    # Calculate pricing
    nightly_rate = float(room_type.price_per_night) if room_type else float(hotel.base_price)
    stay_nights = nights or 1
    base_price = nightly_rate * stay_nights * rooms
    discount = (base_price * hotel.discount_percentage) / 100 if hotel.discount_percentage else 0
    coupon_discount = 0  # Placeholder to be updated when coupon applied
    subtotal = base_price - discount - coupon_discount
    taxes = subtotal * 0.12  # 12% GST
    total = subtotal + taxes

    amenities = hotel.amenities.all()
    food_info = getattr(hotel, 'food_info', None)
    rules_info = getattr(hotel, 'rules', None)
    default_food = [
        "Complimentary breakfast buffet",
        "Pure vegetarian kitchen",
        "24/7 room service",
    ]
    default_rules = [
        "Check-in after 12:00 PM",
        "Valid ID proof required for all guests",
        "No smoking inside rooms",
    ]

    context = {
        'hotel': hotel,
        'selected_room': room_type,
        'room_types': room_queryset,
        'checkin': checkin,
        'checkout': checkout,
        'checkin_date': checkin_date,
        'checkout_date': checkout_date,
        'adults': adults,
        'children': children,
        'rooms': rooms,
        'nights': stay_nights,
        'pricing': {
            'nightly_rate': nightly_rate,
            'base_price': base_price,
            'discount': discount,
            'coupon_discount': coupon_discount,
            'taxes': taxes,
            'total': total,
        },
        'booking_summary': {
            'nights': stay_nights,
            'rooms': rooms,
            'guests_label': f"{adults} Adults" + (f" & {children} Children" if children else ''),
        },
        'amenities': amenities,
        'food_info': food_info or default_food,
        'rules_info': rules_info or default_rules,
        'booking_form_action': reverse('bookings:process'),
        'login_url': reverse('users:login'),
        'signup_url': reverse('users:signup'),
    }

    return render(request, 'bookings/booking_page.html', context)


def process_booking(request):
    """Process booking form submission"""
    if request.method == 'POST':
        # Get form data
        hotel_id = request.POST.get('hotel_id')
        room_type_id = request.POST.get('room_type_id')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        rooms = request.POST.get('rooms')
        
        # Guest details
        title = request.POST.get('title')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        id_type = request.POST.get('id_type')
        id_number = request.POST.get('id_number')
        special_requests = request.POST.get('special_requests', '')
        
        # Payment method
        payment_method = request.POST.get('payment_method')
        
        # Coupon
        coupon_code = request.POST.get('coupon_code', '')
        
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            room_type = RoomType.objects.get(id=room_type_id)
            
            # Calculate dates
            checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()
            nights = (checkout_date - checkin_date).days
            
            # Calculate pricing
            base_price = float(room_type.price_per_night) * nights * int(rooms)
            discount_amount = (base_price * hotel.discount_percentage) / 100
            taxes = (base_price - discount_amount) * 0.12
            
            coupon_discount = 0
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code.upper())
                    if coupon.is_valid():
                        if coupon.discount_type == 'percentage':
                            coupon_discount = (base_price * coupon.discount_value) / 100
                            if coupon.max_discount:
                                coupon_discount = min(coupon_discount, float(coupon.max_discount))
                        else:
                            coupon_discount = float(coupon.discount_value)
                        coupon.used_count += 1
                        coupon.save()
                except Coupon.DoesNotExist:
                    pass
            
            total_amount = base_price - discount_amount - coupon_discount + taxes
            
            # Create booking
            booking = Booking.objects.create(
                user=request.user if request.user.is_authenticated else None,
                hotel=hotel,
                room_type=room_type,
                check_in=checkin_date,
                check_out=checkout_date,
                nights=nights,
                num_adults=adults,
                num_children=children,
                num_rooms=rooms,
                base_price=base_price,
                discount_amount=discount_amount,
                taxes=taxes,
                total_amount=total_amount,
                coupon_code=coupon_code,
                coupon_discount=coupon_discount,
                special_requests=special_requests,
                status='confirmed',
                payment_status='paid' if payment_method != 'payathotel' else 'pending'
            )
            
            # Create guest details
            GuestDetail.objects.create(
                booking=booking,
                title=title,
                full_name=full_name,
                email=email,
                phone=phone,
                id_type=id_type,
                id_number=id_number
            )
            
            # Create payment record
            Payment.objects.create(
                booking=booking,
                payment_method=payment_method,
                amount=total_amount,
                is_successful=True if payment_method != 'payathotel' else False,
                payment_date=timezone.now() if payment_method != 'payathotel' else None
            )
            
            messages.success(request, f'Booking confirmed! Your booking ID is {booking.booking_id}')
            return redirect('bookings:confirmation', booking_id=booking.booking_id)
            
        except Exception as e:
            messages.error(request, f'Booking failed: {str(e)}')
            return redirect('hotels:search')
    
    return redirect('hotels:search')


def booking_confirmation(request, booking_id):
    """Booking confirmation page"""
    booking = get_object_or_404(Booking, booking_id=booking_id)
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'bookings/confirmation.html', context)


def my_bookings(request):
    """User's booking history"""
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    bookings = Booking.objects.filter(user=request.user)
    
    context = {
        'bookings': bookings,
    }
    
    return render(request, 'bookings/my_bookings.html', context)

