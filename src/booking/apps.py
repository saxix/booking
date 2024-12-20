from django.apps import AppConfig


class BookingConfig(AppConfig):
    name = "booking"

    def ready(self) -> None:
        from . import signals  # noqa
