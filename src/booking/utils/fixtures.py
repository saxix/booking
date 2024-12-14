from django.conf import settings

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from booking.models import Accommodation, Booking


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: "name-{n}".format(n=n))

    class Meta:
        model = settings.AUTH_USER_MODEL


class AccommodationFactory(DjangoModelFactory):
    name = factory.Faker("name")
    address = factory.Faker("address")
    description = factory.Faker("text")
    price = factory.fuzzy.FuzzyDecimal(low=30.0, high=130.0, precision=2)
    max_guests = factory.Faker("pyint", min_value=1, max_value=5)

    class Meta:
        model = Accommodation


class BookingFactory(DjangoModelFactory):
    customer = factory.SubFactory(UserFactory)
    property = factory.SubFactory(AccommodationFactory)
    start_date = factory.Faker("date")
    end_date = factory.Faker("date")
    total_price = factory.fuzzy.FuzzyDecimal(low=30.0, high=130.0, precision=2)

    class Meta:
        model = Booking
