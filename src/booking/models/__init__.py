from django.contrib.auth.models import AbstractUser
from django.db import models

from concurrency.fields import VersionField

__all__ = [
    "User",
]


class BaseModel(models.Model):
    version = VersionField()

    class Meta:
        abstract = True


class User(AbstractUser):
    pass


class Customer(BaseModel):
    user = models.ForeignKey


# Modello per le proprietà
class Property(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.name)


# Modello per le prenotazioni
class Booking(BaseModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="bookings")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.property.name} ({self.start_date} - {self.end_date})"


# Modello per i feedback
class Feedback(BaseModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="feedbacks")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    rating = models.PositiveIntegerField()  # Ad esempio: da 1 a 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Feedback for {self.property.name} by {self.customer.username}"
