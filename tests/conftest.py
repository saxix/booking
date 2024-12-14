import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from django.conf import settings

if TYPE_CHECKING:
    from django_webtest.pytest_plugin import MixinWithInstanceVariables
    from booking.models import User
    from django_webtest import DjangoTestApp

here = Path(__file__).parent
sys.path.insert(0, str(here / "../src"))


def pytest_configure():
    pass


@pytest.fixture()
def app(django_app_factory: "MixinWithInstanceVariables", admin_user: "User") -> "DjangoTestApp":
    django_app = django_app_factory(csrf_checks=False)
    django_app.set_user(admin_user)
    django_app._user = admin_user
    yield django_app
