from typing import TYPE_CHECKING, Any, TypeAlias, Union

from environ import Env

if TYPE_CHECKING:
    ConfigItem: TypeAlias = Union[tuple[type, Any],]

CONFIG: "dict[str, ConfigItem]" = {
    "SUPERUSERS": (list, []),
    "DEBUG": (bool, False),
}

env = Env(**CONFIG)
