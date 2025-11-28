"""Forms for user authentication and registration."""

import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import UserProfile

name_validator = RegexValidator(
    regex=r"^[A-Za-z\s]+$",
    message="Name must only contain alphabetical characters and spaces."
)
phone_validator = RegexValidator(
    regex=r"^\d{10}$",
    message="Mobile number must be exactly 10 digits."
)
email_regex_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    message="Please enter a valid email address (e.g., user@example.com)."
)


class LoginForm(forms.Form):
    """Login form supporting username or email identifiers."""

    identifier = forms.CharField(
        label="Email or Username",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "you@example.com or username",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your password",
            }
        ),
    )

    def clean_identifier(self):
        identifier = self.cleaned_data["identifier"].strip()
        if "@" in identifier:
            email_regex_validator(identifier)
        return identifier

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get("identifier")
        password = cleaned_data.get("password")

        if identifier and password:
            user = authenticate(username=identifier, password=password)
            if not user and "@" in identifier:
                try:
                    user_obj = User.objects.get(email__iexact=identifier)
                except User.DoesNotExist:
                    user_obj = None
                if user_obj:
                    user = authenticate(username=user_obj.username, password=password)

            if not user:
                raise forms.ValidationError("Invalid email/username or password.")

            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, "user", None)


class SignupForm(forms.ModelForm):
    """User registration form with extended validation."""

    phone = forms.CharField(
        label="Mobile Number",
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "+91 98765 43210",
                "pattern": "\\d{10}",
                "title": "Mobile number must be exactly 10 digits.",
                "inputmode": "numeric",
                "maxlength": "10",
            }
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Create a strong password",
                "pattern": "(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}",
                "title": "Password must be at least 8 characters with letters and numbers.",
            }
        ),
        help_text="Minimum 8 characters with letters & numbers.",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Re-enter password",
                "pattern": "(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}",
                "title": "Password must be at least 8 characters with letters and numbers.",
            }
        ),
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not phone.isdigit():
            raise forms.ValidationError("Mobile number must contain digits only.")
        phone_validator(phone)
        return phone

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First name",
                    "pattern": "[A-Za-z\\s]+",
                    "title": "Name must only contain alphabetical characters and spaces.",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last name",
                    "pattern": "[A-Za-z\\s]+",
                    "title": "Name must only contain alphabetical characters and spaces.",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Choose a username",
                    "pattern": "[A-Za-z0-9_.-]{3,30}",
                    "title": "Username must be 3-30 characters (letters, numbers, ., _, -).",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "you@example.com",
                    "pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
                    "title": "Please enter a valid email address (e.g., user@example.com).",
                }
            ),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "").strip()
        if first_name:
            name_validator(first_name)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "").strip()
        if last_name:
            name_validator(last_name)
        return last_name

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if not re.match(r"^[A-Za-z0-9_.-]{3,30}$", username):
            raise forms.ValidationError(
                "Username must be 3-30 characters and can include letters, numbers, ., _, -."
            )
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username.lower()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        email_regex_validator(email)
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data["password1"]
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if password.isdigit() or password.isalpha():
            raise forms.ValidationError("Password must include both letters and numbers.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data["phone"]
            profile.save()
        return user


class OTPVerificationForm(forms.Form):
    token = forms.CharField(
        label="Authenticator Code",
        max_length=6,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "6-digit code",
                "inputmode": "numeric",
                "autocomplete": "one-time-code",
            }
        ),
    )

    def clean_token(self):
        token = self.cleaned_data["token"].strip()
        if not token.isdigit() or len(token) != 6:
            raise forms.ValidationError("Enter a valid 6-digit code")
        return token
