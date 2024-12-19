import logging
from typing import Any

from django.core.management import BaseCommand

from booking.utils.fixtures import MODELS

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    requires_migrations_checks = False
    requires_system_checks = []

    def handle(self, *args: Any, **options: Any) -> None:  # noqa
        from booking.utils.fixtures import Car, CarFactory, ServiceFactory

        Car.objects.all().delete()
        CarFactory.create_batch(len(MODELS))
        ServiceFactory.create_batch(10)
