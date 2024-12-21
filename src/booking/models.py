from typing import Any

from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models

from concurrency.fields import AutoIncVersionField

__all__ = ["Booking", "Car", "Feedback", "Service", "User"]


class BaseModel(models.Model):
    version = AutoIncVersionField()

    class Meta:
        abstract = True

    @classmethod
    def retrieve(cls, section: str | None = "") -> Any:
        v = cache.get(f"version:{cls.__name__}")
        return cache.get(f"cache:{v}:{section}")

    @classmethod
    def store(cls, value: Any, section: str | None = "") -> Any:
        v = cache.get(f"version:{cls.__name__}")
        cache.set(f"cache:{v}:{section}", value, timeout=86400)
        cls.invalidate_cache()

    @classmethod
    def invalidate_cache(cls):
        try:
            cache.incr(f"version:{cls.__name__}")
        except ValueError:
            cache.set(f"version:{cls.__name__}", 1)


class User(BaseModel, AbstractUser):
    pass


class Service(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Car(BaseModel):
    description = models.TextField(blank=True, null=True)
    model = models.CharField(max_length=255)
    plate = models.CharField(max_length=10, default="")
    image = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_passenger = models.PositiveIntegerField()
    in_service = models.BooleanField(default=True)
    services = models.ManyToManyField(Service, blank=True)

    def __str__(self) -> str:
        return self.model


class Booking(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="bookings")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(start_date__lte=models.F("end_date"))),
                name="start_date_lte_end_date",
            ),
            models.CheckConstraint(
                check=~(models.Q(start_date=models.F("end_date")) & models.Q(start_date__gt=models.F("end_date"))),
                name="not_start_date_eq_end_date_and_start_date_gt_end_date",
            ),
        ]


class Feedback(BaseModel):
    property = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="feedbacks")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    rating = models.PositiveIntegerField()  # Ad esempio: da 1 a 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
