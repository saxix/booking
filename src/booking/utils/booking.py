from datetime import date

from booking.models import Accommodation, Booking


def is_available(place: Accommodation, start: date, end: date) -> bool:
    return not Booking.objects.filter(property=place, end_date__gte=start, start_date__lte=end).exists()
