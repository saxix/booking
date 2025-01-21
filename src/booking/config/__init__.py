from typing import TYPE_CHECKING, Any

from environ import Env

if TYPE_CHECKING:
    ConfigItem: type = tuple[type, Any]

CONFIG: "dict[str, ConfigItem]" = {
    "SUPERUSERS": (list, []),
    "CACHE_URL": (str, "locmemcache://"),
    "DATABASE_URL": (str, "sqlite:///"),
    "DEBUG": (bool, True),
    "SECRET_KEY": (str, "change-me"),
    "STATIC_ROOT": (str, None),
    "SOCIAL_AUTH_REDIRECT_IS_HTTPS": (bool, True),
    "EXTRA_APPS": (list, []),
    "EXTRA_MIDDLEWARES": (list, []),
    "GOOGLE_CLIENT_ID": (str, ""),
    "GOOGLE_CLIENT_SECRET": (str, ""),
    "GMAIL_USER": (str, ""),
    "GMAIL_PASSWORD": (str, ""),
}

env = Env(**CONFIG)
