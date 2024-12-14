from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from booking.models import Booking, User


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin[Booking]):
    pass


@admin.register(User)
class UserAdmin(_UserAdmin[User]):
    pass
