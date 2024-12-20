from datetime import date, timedelta
from random import randint
from typing import Any

from django.conf import settings
from django.db.models import Model
from django.utils.text import slugify

import factory.fuzzy
from factory.django import DjangoModelFactory

from booking.models import Booking, Car, Service, User


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: "name-{n}@example.com".format(n=n))
    email = factory.Sequence(lambda n: "name-{n}@example.com".format(n=n))
    password = "password"

    class Meta:
        model = settings.AUTH_USER_MODEL

    @classmethod
    def _create(cls, model_class: "Model", *args: Any, **kwargs: Any) -> "User":
        """Create an instance of the model, and save it to the database."""
        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)  # Just user the create_user method recommended by Django


MODELS = ["Audi A5", "Mercedes Coupe SL", "Mercedes S450", "Tesla Model S", "Bmw Sedane", "Range-Rover"]


class CarFactory(DjangoModelFactory):
    model = factory.Iterator(MODELS)
    image = factory.LazyAttribute(lambda o: f"{slugify(o.model)}.png")
    plate = factory.Faker("license_plate")
    price = factory.fuzzy.FuzzyDecimal(low=30.0, high=130.0, precision=2)
    max_passenger = factory.Faker("pyint", min_value=1, max_value=5)

    class Meta:
        model = Car


class BookingFactory(DjangoModelFactory):
    customer = factory.SubFactory(UserFactory)
    car = factory.SubFactory(CarFactory)
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
