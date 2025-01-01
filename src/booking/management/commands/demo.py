import logging
import os
from typing import Any

from django.core.management import BaseCommand

from booking.utils.fixtures import MODELS

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    requires_migrations_checks = False
    requires_system_checks = ()

    def handle(self, *args: Any, **options: Any) -> None:
        from booking.utils.fixtures import Car, CarFactory, Service, ServiceFactory, User

        if "ADMIN_USER" in os.environ:
            User.objects.create_superuser(
                os.environ["ADMIN_USER"],
                email=os.environ["ADMIN_USER"],
                password=os.environ["ADMIN_PASSWORD"],
            )
            self.stdout.write(self.style.SUCCESS("Superuser Successfully created"))
        Car.objects.all().delete()
        CarFactory.create_batch(len(MODELS))
        ServiceFactory.create_batch(10)

        for model in [Car, Service, User]:
            model.invalidate_cache()
