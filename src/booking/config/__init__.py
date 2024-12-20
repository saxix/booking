from typing import TYPE_CHECKING, Any, TypeAlias, Union

from environ import Env

if TYPE_CHECKING:
    ConfigItem: TypeAlias = Union[tuple[type, Any],]

CONFIG: "dict[str, ConfigItem]" = {
    "SUPERUSERS": (list, []),
    "DEBUG": (bool, False),
    "SECRET_KEY": (str, None),
    "STATIC_ROOT": (str, None),
    "SOCIAL_AUTH_REDIRECT_IS_HTTPS": (bool, True),
}

env = Env(**CONFIG)
