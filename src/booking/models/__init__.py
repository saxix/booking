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

class Accommodation(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.name


class Booking(BaseModel):
    property = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="bookings")
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
                        & models.Q(start_time_gt=models.F('end_time'))
                        ),
                name='not_start_date_eq_end_date_and_start_time_gt_end_time'
            ),
        ]

class Feedback(BaseModel):
    property = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="feedbacks")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    rating = models.PositiveIntegerField()  # Ad esempio: da 1 a 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
