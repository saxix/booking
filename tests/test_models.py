import pytest
from django.db import IntegrityError

from booking.models import Booking


@pytest.mark.django_db(transaction=True)
def test_constraints(user, car):
    """Test avoid overlapping booking."""
    Booking.objects.create(customer=user, car=car, start_date="2000-02-01", end_date="2000-02-28", total_price=1)
    Booking.objects.create(customer=user, car=car, start_date="2000-03-01", end_date="2000-03-10", total_price=1)
    # no inner period
    with pytest.raises(IntegrityError):
        Booking.objects.create(customer=user, car=car, start_date="2000-02-05", end_date="2000-02-08", total_price=2)
    # no start overlap
    with pytest.raises(IntegrityError):
        Booking.objects.create(customer=user, car=car, start_date="2000-01-31", end_date="2000-02-03", total_price=2)
    # no end overlap
    with pytest.raises(IntegrityError):
        Booking.objects.create(customer=user, car=car, start_date="2000-02-28", end_date="2000-02-02", total_price=2)
