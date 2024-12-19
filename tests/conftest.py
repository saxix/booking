import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from _pytest.fixtures import SubRequest

if TYPE_CHECKING:
    from django_webtest import DjangoTestApp
    from django_webtest.pytest_plugin import MixinWithInstanceVariables

    from booking.models import Car, User

here = Path(__file__).parent
sys.path.insert(0, str(here / "../src"))


@pytest.fixture
def user(db):
    from booking.utils.fixtures import UserFactory

    return UserFactory()


@pytest.fixture
def car(db):
    from booking.utils.fixtures import CarFactory

    return CarFactory()


@pytest.fixture
def booking(request: SubRequest, car: "Car"):
    from booking.utils.fixtures import BookingFactory

    app: "DjangoTestApp" = request.getfixturevalue("app")

    return BookingFactory(car=car, customer=app._user)


@pytest.fixture()
def app(django_app_factory: "MixinWithInstanceVariables", user: "User") -> "DjangoTestApp":
    django_app = django_app_factory(csrf_checks=False)
    django_app.set_user(user)
    django_app._user = user
    return django_app
