from unittest import mock

from django.urls import reverse
from django_webtest import DjangoTestApp


def test_model_cache(car):
    """Test cache  version is properly increased on change."""
    base = car.get_cache_version()
    assert base
    car.save()
    assert car.get_cache_version() == base + 1


def test_view_cache(app: "DjangoTestApp", car):
    """Test http 304 is properly sent."""
    url = reverse("index")
    with mock.patch("booking.models.Car.objects.values") as m:
        res = app.get(url, user=None)
        assert res.status_code == 200  # check
        assert (etag := res["Etag"])
        assert m.call_count == 1

        res = app.get(url, user=None, headers={"IF_NONE_MATCH": etag})
        assert res.status_code == 304
        assert m.call_count == 1


def test_view_index(app: "DjangoTestApp", car):
    """Test application cache is triggered."""
    url = reverse("index")
    with mock.patch("booking.models.Car.get_from_cache") as m:
        res = app.get(url, user=None)
        assert res.status_code == 200  # check
        assert m.call_count == 1

        res = app.get(url, user=None, headers={})
        assert res.status_code == 200
        assert m.call_count == 2
