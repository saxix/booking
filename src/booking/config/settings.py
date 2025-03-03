from pathlib import Path

from . import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
SUPERUSERS = env("SUPERUSERS")

ALLOWED_HOSTS: list[str] = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tailwind",
    "social_django",
    "booking.theme",
    "booking",
    *env("EXTRA_APPS"),
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    *env("EXTRA_MIDDLEWARES"),
]

ROOT_URLCONF = "booking.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "booking.config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": env.db(),
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)
AUTH_USER_MODEL = "booking.User"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LANGUAGE_CODE = "en-us"
LANGUAGE_COOKIE_NAME = "booking-language"
LANGUAGES = (
    ("en-us", "English"),
    ("it-it", "Italian"),
)
LOCALE_PATHS = (str(BASE_DIR / "LOCALE"),)

CACHES = {"default": env.cache("CACHE_URL")}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = env("STATIC_ROOT")

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"
LOGOUT_REDIRECT_URL = "/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
TAILWIND_APP_NAME = "booking.theme"
TAILWIND_CSS_PATH = "css/styles.css"

SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_REQUIRE_POST = False
SOCIAL_AUTH_REDIRECT_IS_HTTPS = env("SOCIAL_AUTH_REDIRECT_IS_HTTPS")
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("GOOGLE_CLIENT_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "booking.utils.pipeline.configure_user",
)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("GMAIL_USER")
EMAIL_HOST_PASSWORD = env("GMAIL_PASSWORD")
