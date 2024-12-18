from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from booking.models import Car, Booking, User, Service


@admin.register(User)
class UserAdmin(_UserAdmin[User]):
    search_fields = ("username",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin[Booking]):
    list_display = ("property", "customer", "start_date", "end_date")
    autocomplete_fields = ["customer", "property"]


@admin.register(Car)
class CarAdmin(admin.ModelAdmin[Car]):
    search_fields = ("model",)
    list_display = ("model", "image", "price", "max_passenger", "in_service")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin[Service]):
    search_fields = ("name",)
