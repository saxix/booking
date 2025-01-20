from datetime import date, timedelta
from random import randint
from typing import Any

import factory.fuzzy
from django.conf import settings
from django.db.models import Model
from django.utils.text import slugify
from django.utils.translation import gettext as _
from factory.django import DjangoModelFactory

from booking.models import Booking, Car, Service, User


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: f"name-{n}@example.com")
    email = factory.Sequence(lambda n: f"name-{n}@example.com")
    _password = "password"  # noqa

    class Meta:
        model = settings.AUTH_USER_MODEL

    @classmethod
    def _create(cls, model_class: "Model", *args: Any, **kwargs: Any) -> "User":
        """Create an instance of the model, and save it to the database."""
        if cls._meta.django_get_or_create:
            user = cls._get_or_create(model_class, *args, **kwargs)
        else:
            manager = cls._get_manager(model_class)
            user = manager.create_user(*args, **kwargs)  # Just user the create_user method recommended by Django

        user.set_password(UserFactory._password)
        user._password = UserFactory._password
        user.save()
        return user


MODELS = [
    "Audi A5",
    "Mercedes Coupe SL",
    "Mercedes S450",
    "Tesla Model S",
    "Bmw Sedane",
    "Range-Rover",
]


class CarFactory(DjangoModelFactory):
    model = factory.Iterator(MODELS)
    image = factory.LazyAttribute(lambda o: f"{slugify(o.model)}.jpg")
    plate = factory.Faker("license_plate")
    price = factory.fuzzy.FuzzyDecimal(low=30.0, high=130.0, precision=2)
    max_passenger = factory.Faker("pyint", min_value=1, max_value=5)

    class Meta:
        model = Car


class BookingFactory(DjangoModelFactory):
    customer = factory.SubFactory(UserFactory)
    car = factory.SubFactory(CarFactory)
    start_date = factory.fuzzy.FuzzyDate(date(2025, 1, 1), date(2025, 8, 1))
    end_date = factory.LazyAttribute(lambda i: i.start_date + timedelta(days=randint(1, 10)))  # noqa
    total_price = factory.fuzzy.FuzzyDecimal(low=30.0, high=130.0, precision=2)

    class Meta:
        model = Booking


class ServiceFactory(DjangoModelFactory):
    name = factory.Iterator([_("bar"), _("TV"), _("seat warmers"), _("ski rack")])

    class Meta:
        model = Service
        django_get_or_create = ["name"]
