from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from booking.models import Accommodation, Booking, User, Service


@admin.register(User)
class UserAdmin(_UserAdmin[User]):
    search_fields = ("username",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin[Booking]):
    list_display = ("property", "customer", "start_date", "end_date")
    autocomplete_fields = ["customer", "property"]


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin[Accommodation]):
    search_fields = ("name",)
    list_display = ("name", "address", "price", "max_guests")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin[Service]):
    search_fields = ("name",)
