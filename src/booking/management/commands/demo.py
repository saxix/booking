import logging
from typing import Any

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    requires_migrations_checks = False
    requires_system_checks = []

    def handle(self, *args: Any, **options: Any) -> None:  # noqa
        from booking.utils.fixtures import Accommodation, AccommodationFactory, ServiceFactory

        Accommodation.objects.all().delete()
        ServiceFactory.create_batch(10)
        AccommodationFactory.create_batch(10)
