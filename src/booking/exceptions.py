from typing import Any

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PeriodNotAvailable(ValidationError):
    """Raises when period is not available."""


class RecordChanged(ValidationError):
    message = _("Selected car details hae been updated. Please check before proceeding.")

    def __init__(
        self,
        message: str | None = None,
        code: str | None = None,
        params: Any | None = None,
    ) -> None:
        msg = message or self.message
        super().__init__(msg, code, params)
