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


class Service(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Car(BaseModel):
    description = models.TextField()
    model = models.CharField(max_length=255)
    plate = models.CharField(max_length=10, default="")
    image = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_passenger = models.PositiveIntegerField()
    in_service = models.BooleanField(default=True)
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.model


class Booking(BaseModel):
    property = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="bookings")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(start_date__lte=models.F('end_date'))),
                name='start_date_lte_end_date'
            ),
            models.CheckConstraint(
                check=~(models.Q(start_date=models.F('end_date'))
                        & models.Q(start_date__gt=models.F('end_date'))
                        ),
                name='not_start_date_eq_end_date_and_start_date_gt_end_date'
            ),
        ]

class Feedback(BaseModel):
    property = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="feedbacks")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    rating = models.PositiveIntegerField()  # Ad esempio: da 1 a 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
