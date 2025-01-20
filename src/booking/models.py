from typing import Any

from concurrency.fields import AutoIncVersionField
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import RangeOperators
from django.core.cache import cache
from django.db import models

__all__ = ["Booking", "Car", "Service", "User"]


class BaseModel(models.Model):
    """Base model implementing Template Method Pattern to provide caching capabilities."""

    version = AutoIncVersionField()

    class Meta:
        abstract = True

    @classmethod
    def get_cache_version(cls) -> int:
        """Retrieve an entry from the cache.

        :param label eventuale label per individuare una sottochiave
        :type label: string
        :return numero di versione per la entry selezionata
        :rtype: int
        """
        return cache.get(f"version:{cls.__name__}") or 1

    @classmethod
    def invalidate_cache(cls):
        """Invalidate all cache entries for the object."""
        try:
            cache.incr(f"version:{cls.__name__}")
        except ValueError:
            cache.set(f"version:{cls.__name__}", 1)

    @classmethod
    def get_from_cache(cls, label: str | None = "") -> Any:
        """Recupera una voce dalla cache.

        :param label eventuale label per individuare una sottochiave
        :type label: string
        :return: Valore registrato nella cache o None
        :rtype: Any
        """
        v = cls.get_cache_version()
        return cache.get(f"cache:{label}", version=v)

    @classmethod
    def store_to_cache(cls, value: Any, label: str | None = "") -> None:
        """Memorizza `value` nella cache, eventualmente etichettandolo.

        :param value Valore da inserire nella cache
        :type value Any
        :param label eventuale label per individuare una sottochiave
        :type label: string
        :return: None
        """
        v = cls.get_cache_version()
        cache.set(f"cache:{label}", value, timeout=86400, version=v)


class User(BaseModel, AbstractUser):
    pass


class Service(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Car(BaseModel):
    """Car model. It represents the Car Business Object."""

    model = models.CharField(max_length=255, help_text="Model of the car.")
    plate = models.CharField(max_length=10, default="", help_text="Plate of the car.")
    image = models.CharField(max_length=255, blank=True, help_text="Image of the car.")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Daily price of the car.")
    max_passenger = models.PositiveIntegerField(help_text="Maximum number of passengers allowed in the car.")
    in_service = models.BooleanField(default=True, help_text="Whether the car is in service.")
    services = models.ManyToManyField(Service, blank=True, help_text="Services related to the car.")

    def __str__(self) -> str:
        return self.model


class Booking(BaseModel):
    """Representa la prenotazione."""

    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="bookings", help_text="Car related to the booking."
    )
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings", help_text="The customer who owns the booking."
    )
    start_date = models.DateField(help_text="Start date of the booking.")
    end_date = models.DateField(help_text="End date of the booking.")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, help_text="Total price of the booking."
    )

    class Meta:
        constraints = [
            # primo vincolo: la data di fine prenotazione deve essere dopo la data di inizio
            models.CheckConstraint(
                check=(models.Q(start_date__lte=models.F("end_date"))),
                name="start_date_lte_end_date",
            ),
            # secondo vincolo non ci possono essre periodi sovrapposti per lo stesso veicolo
            ExclusionConstraint(
                name="prevent_overlapping_bookings",
                expressions=[
                    ("car", RangeOperators.EQUAL),  # Auto deve essere la stessa
                    (
                        models.Func(models.F("start_date"), models.F("end_date"), function="DATERANGE"),
                        RangeOperators.OVERLAPS,
                    ),
                ],
            ),
        ]
