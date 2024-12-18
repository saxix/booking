from datetime import timedelta
from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

import pytest
from django.utils import timezone
from django_webtest import DjangoTestApp

from booking.exceptions import RecordChanged

if TYPE_CHECKING:
    from booking.models import Car, Booking


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


def test_book_create(app: "DjangoTestApp", place: "Car"):
    url = reverse("booking-add", args=[place.pk])
    res = app.get(url)
    ver = place.version
    assert res.status_code == 200, res.location
    res.forms[0]["start_date"] = timezone.now().date()
    res.forms[0]["end_date"] = timezone.now().date() + timedelta(days=1)
    res = res.forms[0].submit()
    assert res.status_code == 302, res.showbrowser()
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


def test_book_avoid_overlapping(app: "DjangoTestApp", booking: "Booking"):
    url = reverse("booking-add", args=[booking.property.pk])
    res = app.get(url)
    res.forms[0]["start_date"] = booking.start_date
    res.forms[0]["end_date"] = booking.start_date + timedelta(days=1)
    res = res.forms[0].submit()
    assert res.status_code == 200
    assert "Selected period is not available" in res.text

def test_book_avoid_overlapping(app: "DjangoTestApp", booking: "Booking"):
    url = reverse("booking-add", args=[booking.property.pk])
    res = app.get(url)
    res.forms[0]["start_date"] = booking.start_date
    res.forms[0]["end_date"] = booking.start_date + timedelta(days=1)
    res = res.forms[0].submit()
    assert res.status_code == 200
    assert "Selected period is not available" in res.text

def test_book_place_changed(app: "DjangoTestApp", place: "Car"):
    url = reverse("booking-add", args=[place.pk])
    res = app.get(url)
    place.price = 101.1
    place.save()
    res.forms[0]["start_date"] = timezone.now().date()
    res.forms[0]["end_date"] = timezone.now().date() + timedelta(days=1)
    res = res.forms[0].submit()
    assert res.status_code == 200
    assert RecordChanged.message in res.text, res.showbrowser()
