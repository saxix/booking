from unittest import mock

from django.urls import reverse
from django_webtest import DjangoTestApp


def test_model_cache(car):
    base = car.get_cache_version()
    assert base
    car.save()
    assert car.get_cache_version() == base + 1


def test_view_cache(app: "DjangoTestApp", car):
    url = reverse("index")
    with mock.patch("booking.models.Car.objects.values") as m:
        res = app.get(url, user=None)
        assert res.status_code == 200  # check
        assert (etag := res["Etag"])
        m.assert_called_once()

        res = app.get(url, user=None, headers={"IF_NONE_MATCH": etag})
        assert res.status_code == 304
        assert m.call_count == 1
