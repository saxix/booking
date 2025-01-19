"""Handlers per il sottosistema dei Signals di Django.

@see https://docs.djangoproject.com/en/4.2/ref/signals/

"""

from typing import Any

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import BaseModel, Booking, Car, User


@receiver(post_save, sender=Car)
@receiver(post_save, sender=Booking)
@receiver(post_save, sender=User)
@receiver(post_delete, sender=Booking)
@receiver(post_delete, sender=Car)
def invalidate_car_cache(sender: BaseModel, **kwargs: Any) -> None:
    """Signal handler to invalidate cache on object update."""
    sender.invalidate_cache()
