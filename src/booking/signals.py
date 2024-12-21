from typing import Any

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BaseModel, Booking, Car, User


@receiver(post_save, sender=Car)
@receiver(post_save, sender=Booking)
@receiver(post_save, sender=User)
def invalidate_car_cache(sender: BaseModel, **kwargs: Any) -> None:
    try:
        sender.invalidate_cache()
    except ValueError:
        cache.set("version:fleet", 1)
