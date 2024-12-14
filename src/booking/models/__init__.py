from django.contrib.auth.models import AbstractUser
from django.db import models

from concurrency.fields import AutoIncVersionField

__all__ = [
    "User",
]


class BaseModel(models.Model):
    version = AutoIncVersionField()

    class Meta:
        abstract = True


class User(AbstractUser):
    pass


class Accommodation(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)


# Modello per le prenotazioni
class Booking(BaseModel):
    property = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="bookings")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


# Modello per i feedback
class Feedback(BaseModel):
    property = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="feedbacks")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    rating = models.PositiveIntegerField()  # Ad esempio: da 1 a 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
