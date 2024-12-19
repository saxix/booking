from datetime import date

from booking.models import Car, Booking


def is_available(car: Car, start: date, end: date) -> bool:
    return (start and end) and not Booking.objects.filter(car=car, end_date__gte=start, start_date__lte=end).exists()
