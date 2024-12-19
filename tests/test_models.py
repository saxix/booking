import pytest
from django.db import IntegrityError

from booking.models import Booking


def test_constraints(user, car):
    Booking.objects.create(customer=user, car=car, start_date="2000-01-01", end_date="2000-01-31",
                           total_price=1)
    Booking.objects.create(customer=user, car=car, start_date="2000-01-31", end_date="2000-02-10",
                           total_price=1)
    with pytest.raises(IntegrityError):
        Booking.objects.create(customer=user, car=car, start_date="2000-10-01", end_date="2000-02-10",
                               total_price=2)
