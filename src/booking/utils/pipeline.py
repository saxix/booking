from typing import Any, Optional

from django.conf import settings
from django.contrib.auth.models import User


def configure_user(user: Optional[User] = None, **kwargs: Any) -> dict[str, Any]:
    if user and user.email in settings.SUPERUSERS:
        user.is_staff = True
        user.is_superuser = True
        user.save()
    return {}
