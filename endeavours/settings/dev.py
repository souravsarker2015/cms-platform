"""Local development settings."""

from .base import *
from .base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE, env  # noqa: F401

DEBUG = True

# A default is provided so a fresh clone runs without a .env file. Never reuse
# this value outside local development.
SECRET_KEY = env.str(
    "SECRET_KEY",
    default="django-insecure-dev-only-key-do-not-use-in-production",
)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "0.0.0.0", "[::1]"],
)

# Django 6.1+ mailer config. EMAIL_BACKEND is deprecated (removed in 7.0).
MAILERS = {
    "default": {"BACKEND": "django.core.mail.backends.console.EmailBackend"},
}

# Wagtail's page editor previews need the dev server to answer its own requests.
WAGTAILADMIN_BASE_URL = env.str("WAGTAILADMIN_BASE_URL", default="http://localhost:8000")

# django-debug-toolbar is a dev-only dependency; skip it when not installed.
try:
    import debug_toolbar  # noqa: F401
except ImportError:
    pass
else:
    INSTALLED_APPS = [*INSTALLED_APPS, "debug_toolbar"]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]
    INTERNAL_IPS = ["127.0.0.1", "::1"]

try:
    from .local import *
except ImportError:
    pass
