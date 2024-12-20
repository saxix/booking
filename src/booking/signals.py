from typing import Any

from django.core.cache import cache
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Booking, Car, User


@receiver(post_save, sender=Car)
@receiver(post_save, sender=Booking)
def invalidate_csr_cache(**kwargs: Any) -> None:
    try:
        cache.incr("version:fleet")
    except ValueError:
        cache.set("version:fleet", 1)


@receiver(post_save, sender=Booking)
def invalidate_booking_cache(sender: Model, instance: Booking, **kwargs: Any) -> None:
    try:
        cache.incr(f"version:booking:{instance.customer.pk}")
    except ValueError:
        cache.set(f"version:booking:{instance.customer.pk}", 1)


@receiver(post_save, sender=User)
def invalidate_cache(sender: Model, instance: User, **kwargs: Any) -> None:
    try:
        cache.incr(f"version:user:{instance.pk}")
    except ValueError:
        cache.set(f"version:user:{instance.pk}", 1)
