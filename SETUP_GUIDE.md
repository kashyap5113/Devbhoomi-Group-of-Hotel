# Dwarka Getaways - Django Setup Guide

## 📁 Project Structure

```
dwarka_getaways/
│
├── dwarka_getaways/          # Main project folder
│   ├── __init__.py
│   ├── settings.py          # ✅ Created - Project settings
│   ├── urls.py              # ✅ Created - Main URL configuration
│   ├── wsgi.py              # Auto-generated
│   └── asgi.py              # Auto-generated
│
├── core/                     # Core app (Homepage, About, Contact)
│   ├── __init__.py
│   ├── models.py            # ✅ Created - Destination, ContactMessage
│   ├── views.py             # ✅ Created - Homepage, About, Contact views
│   ├── urls.py              # ✅ Created - Core URLs
│   ├── admin.py             # ✅ Created - Admin configuration
│   ├── apps.py              # Auto-generated
│   ├── tests.py             # Auto-generated
│   └── migrations/          # Auto-generated
│
├── hotels/                   # Hotels app (Search, Details, Reviews)
│   ├── __init__.py
│   ├── models.py            # ✅ Created - Hotel, RoomType, Amenity, Review
│   ├── views.py             # ✅ Created - Search, Filter, Details views
│   ├── urls.py              # ✅ Created - Hotels URLs
│   ├── admin.py             # ✅ Created - Admin configuration
│   ├── apps.py              # Auto-generated
│   ├── tests.py             # Auto-generated
│   └── migrations/          # Auto-generated
│
├── bookings/                 # Bookings app (Booking process, Payment)
│   ├── __init__.py
│   ├── models.py            # ✅ Created - Booking, GuestDetail, Payment, Coupon
│   ├── views.py             # ✅ Created - Booking, Confirmation views
│   ├── urls.py              # ✅ Created - Bookings URLs
│   ├── admin.py             # ✅ Created - Admin configuration
│   ├── apps.py              # Auto-generated
│   ├── tests.py             # Auto-generated
│   └── migrations/          # Auto-generated
│
├── users/                    # Users app (Login, Signup, Profile)
│   ├── __init__.py
│   ├── models.py            # ✅ Created - UserProfile
│   ├── views.py             # ✅ Created - Login, Signup, Profile views
│   ├── urls.py              # ✅ Created - Users URLs
│   ├── admin.py             # ✅ Created - Admin configuration
│   ├── apps.py              # Auto-generated
│   ├── tests.py             # Auto-generated
│   └── migrations/          # Auto-generated
│
├── templates/                # HTML templates (to be created)
│   ├── base.html
│   ├── home/
│   │   ├── index.html
│   │   ├── about_dwarka.html
│   │   └── contact.html
│   ├── hotels/
│   │   ├── search_results.html
│   │   └── hotel_details.html
│   ├── bookings/
│   │   ├── booking_page.html
│   │   ├── confirmation.html
│   │   └── my_bookings.html
│   └── users/
│       ├── login.html
│       ├── signup.html
│       └── profile.html
│
├── static/                   # Static files (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                    # User uploaded files
│   ├── hotels/
│   ├── destinations/
│   └── profiles/
│
├── manage.py                # Django management script
├── requirements.txt         # ✅ Created - Python dependencies
└── db.sqlite3              # Database (auto-generated)
```

---

## 🚀 Step-by-Step Setup Instructions

### **Step 1: Install Python**
Make sure you have Python 3.8+ installed.
```bash
python --version
```

### **Step 2: Create Project Directory**
```bash
mkdir dwarka_getaways
cd dwarka_getaways
```

### **Step 3: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### **Step 4: Install Django**
```bash
pip install django Pillow
```

### **Step 5: Create Django Project**
```bash
django-admin startproject dwarka_getaways .
```
**Note the dot (.) at the end - this creates the project in the current directory**

### **Step 6: Create Apps**
```bash
python manage.py startapp core
python manage.py startapp hotels
python manage.py startapp bookings
python manage.py startapp users
```

### **Step 7: Copy All Code Files**
Now copy all the code I provided into their respective files:

1. **dwarka_getaways/settings.py** - Replace with provided settings
2. **dwarka_getaways/urls.py** - Replace with provided URLs
3. **core/models.py** - Copy models
4. **core/views.py** - Copy views
5. **core/urls.py** - Create and copy
6. **core/admin.py** - Copy admin config
7. **hotels/models.py** - Copy models
8. **hotels/views.py** - Copy views
9. **hotels/urls.py** - Create and copy
10. **hotels/admin.py** - Copy admin config
11. **bookings/models.py** - Copy models
12. **bookings/views.py** - Copy views
13. **bookings/urls.py** - Create and copy
14. **bookings/admin.py** - Copy admin config
15. **users/models.py** - Copy models
16. **users/views.py** - Copy views
17. **users/urls.py** - Create and copy
18. **users/admin.py** - Copy admin config

### **Step 8: Create Directories**
```bash
mkdir templates
mkdir templates/home
mkdir templates/hotels
mkdir templates/bookings
mkdir templates/users
mkdir static
mkdir static/css
mkdir static/js
mkdir static/images
mkdir media
```

### **Step 9: Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **Step 10: Create Superuser**
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### **Step 11: Run Development Server**
```bash
python manage.py runserver
```

### **Step 12: Access the Application**
- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 🗂️ What Each App Does

### **Core App**
- Homepage with featured hotels
- About Dwarka information page
- Contact form
- Destinations management

### **Hotels App**
- Hotel listings with filters
- Search functionality
- Hotel details page
- Room types management
- Reviews system
- Amenities management

### **Bookings App**
- Booking process
- Guest information collection
- Payment processing
- Coupon system
- Booking confirmation
- Booking history

### **Users App**
- User registration
- Login/Logout
- User profile management
- Password change
- Account deletion

---

## 📊 Admin Panel Features

Login to admin panel at: http://127.0.0.1:8000/admin/

You can manage:
- ✅ Hotels (add, edit, delete)
- ✅ Room Types
- ✅ Amenities
- ✅ Reviews (approve/disapprove)
- ✅ Bookings (view, update status)
- ✅ Coupons (create discount codes)
- ✅ Users & Profiles
- ✅ Destinations
- ✅ Contact Messages

---

## 🎨 Next Steps

1. **Create HTML Templates** - Copy your existing HTML files into templates folder
2. **Update Templates** - Add Django template tags
3. **Add Sample Data** - Add hotels, amenities through admin
4. **Test Functionality** - Test all features
5. **Deploy** - Deploy to production server

---

## 🐛 Troubleshooting

### Error: "No module named 'PIL'"
```bash
pip install Pillow
```

### Error: "App isn't loaded"
Make sure all apps are added to `INSTALLED_APPS` in settings.py

### Error: "Table doesn't exist"
Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error: "Static files not found"
Run:
```bash
python manage.py collectstatic
```

---

## 📝 URL Structure

### Core URLs:
- `/` - Homepage
- `/about-dwarka/` - About page
- `/contact/` - Contact page

### Hotels URLs:
- `/hotels/search/` - Search results
- `/hotels/<hotel-slug>/` - Hotel details

### Bookings URLs:
- `/bookings/<hotel-slug>/` - Booking page
- `/bookings/process/` - Process booking
- `/bookings/confirmation/<booking-id>/` - Confirmation
- `/bookings/my-bookings/` - User bookings

### Users URLs:
- `/users/login/` - Login page
- `/users/signup/` - Registration
- `/users/profile/` - User profile
- `/users/logout/` - Logout

---

## ✅ Checklist

- [ ] Python installed
- [ ] Virtual environment created
- [ ] Django installed
- [ ] Project created
- [ ] Apps created
- [ ] All code files copied
- [ ] Migrations run
- [ ] Superuser created
- [ ] Server running
- [ ] Admin panel accessible
- [ ] Templates created
- [ ] Static files configured
- [ ] Sample data added

---

## 🎉 You're All Set!

Your Django backend for Dwarka Getaways is now ready!
Next, integrate your HTML templates and start testing! 🚀