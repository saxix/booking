from datetime import datetime, timedelta, date
from random import randint

from django.conf import settings

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from booking.models import Accommodation, Booking, Service


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: "name-{n}".format(n=n))

    class Meta:
        model = settings.AUTH_USER_MODEL


class AccommodationFactory(DjangoModelFactory):
    name = factory.Faker("first_name")
    address = factory.Faker("address")
    city = factory.Faker("city")
    description = factory.Faker("text")
    price = factory.fuzzy.FuzzyDecimal(low=30.0, high=130.0, precision=2)
    max_guests = factory.Faker("pyint", min_value=1, max_value=5)

    class Meta:
        model = Accommodation


class BookingFactory(DjangoModelFactory):
    customer = factory.SubFactory(UserFactory)
    property = factory.SubFactory(AccommodationFactory)
    start_date = factory.fuzzy.FuzzyDate(date(2025, 1, 1), date(2025, 8, 1))
    end_date = factory.LazyAttribute(lambda i: i.start_date + timedelta(days=randint(1, 10)))
    total_price = factory.fuzzy.FuzzyDecimal(low=30.0, high=130.0, precision=2)

    class Meta:
        model = Booking


class ServiceFactory(DjangoModelFactory):
    name = factory.Iterator(["wifi", "TV", "Laundry", "Pool", "Daily cleaning"])

    class Meta:
        model = Service
        django_get_or_create = ["name"]
