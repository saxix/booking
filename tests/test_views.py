from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

import pytest
from django_webtest import DjangoTestApp

if TYPE_CHECKING:
    from booking.models import Accommodation, Booking


def test_index(app: "DjangoTestApp"):
    url = reverse("index")
    res = app.get(url, user="")
    assert res.status_code == 200

    res = app.get(url)
    assert res.status_code == 302


def test_book_list(app: "DjangoTestApp", booking: "Booking"):
    url = reverse("booking-list")
    res = app.get(url)

    assert res.status_code == 200, res.location


def test_book_create(app: "DjangoTestApp", place: "Accommodation"):
    url = reverse("booking-add", args=[place.pk])
    res = app.get(url)
    ver = place.version
    assert res.status_code == 200, res.location
    res = res.forms[0].submit()
    assert res.status_code == 302
    assert res.location == reverse("booking-list")

    place.refresh_from_db()
    assert place.bookings.count() == 1
    assert place.version != ver


def test_book_cancel(app: "DjangoTestApp", booking: "Booking"):
    url = reverse("booking-cancel", args=[booking.pk])
    res = app.get(url)

    assert res.status_code == 200, res.location
    res = res.forms[0].submit()
    assert res.status_code == 302
    assert res.location == reverse("booking-list")

    with pytest.raises(ObjectDoesNotExist):
        booking.refresh_from_db()
