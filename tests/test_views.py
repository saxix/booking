import threading
from datetime import timedelta
from unittest import mock

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django_webtest import DjangoTestApp

from booking.exceptions import RecordChanged
from booking.models import Booking, Car


def test_index(app: "DjangoTestApp"):
    url = reverse("index")
    res = app.get(url, user="")
    assert res.status_code == 200

    res = app.get(url)
    assert res.status_code == 200


def test_fleet(app: "DjangoTestApp", car: "Car"):
    url = reverse("car-list")
    res = app.get(url)
    assert res.status_code == 200, res.location
    res = app.get(url)
    assert res.status_code == 200, res.location


def test_healthcheck(app: "DjangoTestApp", car: "Car"):
    url = reverse("healthcheck")
    res = app.get(url)
    assert res.status_code == 200, res.location


def test_book_list(app: "DjangoTestApp", booking: "Booking"):
    url = reverse("booking-list")
    res = app.get(url)

    assert res.status_code == 200, res.location


def test_book_create(app: "DjangoTestApp", car: "Car"):
    url = reverse("booking-add", args=[car.pk])
    res = app.get(url)
    assert res.status_code == 200, res.location
    res.forms[0]["start_date"] = timezone.now().date()
    res.forms[0]["end_date"] = timezone.now().date() + timedelta(days=1)
    res = res.forms[0].submit()
    assert res.status_code == 302, res.showbrowser()
    assert res.location == reverse("booking-list")

    car.refresh_from_db()
    assert car.bookings.count() == 1


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
    url = reverse("booking-add", args=[booking.car.pk])
    res = app.get(url)
    res.forms[0]["start_date"] = booking.start_date
    res.forms[0]["end_date"] = booking.start_date + timedelta(days=1)
    res = res.forms[0].submit()
    assert res.status_code == 200
    assert "Selected period is not available" in res.text


def test_book_car_changed(app: "DjangoTestApp", car: "Car"):
    url = reverse("booking-add", args=[car.pk])
    res = app.get(url)
    car.price = 101.1
    car.save()
    res.forms[0]["start_date"] = timezone.now().date()
    res.forms[0]["end_date"] = timezone.now().date() + timedelta(days=1)
    res = res.forms[0].submit()
    assert res.status_code == 200
    assert RecordChanged.message in res.text, res.showbrowser()


def test_etag(app: "DjangoTestApp", car: "Car"):
    url = reverse("index")
    res = app.get(url, user=None)
    assert (etag := res["Etag"])
    assert res.status_code == 200
    res = app.get(url, user=None, headers={"IF_NONE_MATCH": etag})
    assert res.status_code == 304

    car.save()  # force cache invalidation
    res = app.get(url, user=None, headers={"IF_NONE_MATCH": etag})
    assert res.status_code == 200
    assert res["Etag"] != etag


@pytest.mark.django_db(transaction=True)
def test_concurrency(app, car):
    url = reverse("booking-add", args=[car.id])
    with (
        mock.patch(
            "django.views.generic.edit.FormMixin.form_valid",
        ) as m1,
        mock.patch("django.views.generic.edit.FormMixin.form_invalid") as m2,
    ):
        m1.return_value = HttpResponse("Ok", status=302)
        m2.return_value = HttpResponse("Ok", status=200)

        def t1():
            return app.post(url, {"car_version": car.version, "start_date": "2000-01-01", "end_date": "2000-01-31"})

        threads = [threading.Thread(target=t1) for __ in range(10)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        assert m1.call_count >= 1
        assert m2.call_count >= 1
