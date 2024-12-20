from typing import Any, Optional

from django.core.exceptions import ValidationError


class PeriodNotAvailable(ValidationError):
    pass


class RecordChanged(ValidationError):
    message = "Selected place infos hae been updated. Please check before proceeding."

    def __init__(self, message: Optional[str] = None, code: Optional[str] = None, params: Optional[Any] = None) -> None:
        msg = message or self.message
        super().__init__(msg, code, params)
