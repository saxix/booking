from typing import Any

from django.core.exceptions import ValidationError


class PeriodNotAvailable(ValidationError):
    pass


class RecordChanged(ValidationError):
    message = "Selected place infos hae been updated. Please check before proceeding."

    def __init__(
        self,
        message: str | None = None,
        code: str | None = None,
        params: Any | None = None,
    ) -> None:
        msg = message or self.message
        super().__init__(msg, code, params)
