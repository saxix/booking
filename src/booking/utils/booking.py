from datetime import date

from booking.models import Booking, Car


def is_available(car: Car, start: date | None, end: date | None) -> bool:
    return (
        bool(start and end) and not Booking.objects.filter(car=car, end_date__gte=start, start_date__lte=end).exists()
    )
