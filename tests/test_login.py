from unittest import mock

import pytest
from django.conf import settings
from django.test import override_settings
from django.urls import reverse
from webob.exc import strip_tags

from booking.models import User
from booking.utils.fixtures import UserFactory
from booking.utils.pipeline import configure_user


@pytest.fixture
def user(db):
    return UserFactory()


@override_settings(SOCIAL_AUTH_GOOGLE_OAUTH2_KEY="1", SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET="2")
def test_login(db, client):
    session = client.session
    session["google-oauth2_state"] = "1"
    session.save()

    res = client.get(reverse("social:begin", kwargs={"backend": "google-oauth2"}))
    assert res.status_code == 302

    with mock.patch("social_core.backends.base.BaseAuth.request") as mock_request:
        url = reverse("social:complete", kwargs={"backend": "google-oauth2"})
        url += "?code=2&state=1"
        mock_request.return_value.json.return_value = {"access_token": "123"}
        with mock.patch(
            "django.contrib.sessions.backends.base.SessionBase.set_expiry",
            side_effect=[OverflowError, None],
        ):
            response = client.get(url)
            assert response.status_code == 302
            assert response.url == settings.LOGIN_REDIRECT_URL


def test_pipeline(user, settings):
    settings.SUPERUSERS = [user.email]
    configure_user(user)
    user.refresh_from_db()
    assert user.is_superuser


def test_login_email(app, user):
    url = reverse("login")
    app.set_user(None)
    res = app.get(url)
    res.forms["login-form"]["username"] = user.username
    res.forms["login-form"]["password"] = "password"
    res = res.forms["login-form"].submit()
    assert res.status_code == 302


def test_register(app, mailoutbox):
    username = "user@example.com"
    password = "password"
    res = app.get(reverse("register"), user=None)
    res.forms["register-form"]["username"] = username
    res.forms["register-form"]["password"] = password
    res = res.forms["register-form"].submit()
    assert res.status_code == 302
    assert User.objects.filter(email=username, username=username, is_active=True).exists()
    # Check OTP email and link
    assert len(mailoutbox) == 1
    url = strip_tags(mailoutbox[0].body).replace("Per accedere fai click su questo link", "").strip()
    res = app.get(url, user=None)
    assert res.status_code == 302

    # Check standard login
    res = app.get(reverse("login"), user=None)
    res.forms["login-form"]["username"] = username
    res.forms["login-form"]["password"] = password
    res = res.forms["login-form"].submit()
    assert res.status_code == 302


def test_invalid_or_expired_otp(app, mailoutbox):
    url = reverse("otp-login", args=["abc"])
    res = app.get(url, user=None, expect_errors=True)
    assert res.status_code == 404
