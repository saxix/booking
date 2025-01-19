"""Confiurazione per l'admin integrato di Django.

@see https://docs.djangoproject.com/en/4.2/ref/contrib/admin/

"""

from django.apps import AppConfig


class BookingConfig(AppConfig):
    name = "booking"

    def ready(self) -> None:
        from . import handlers  # noqa
