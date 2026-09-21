"""
Staging settings.

Mirrors production but tolerates a throwaway database: SQLite is permitted here
so a staging box can run without a Postgres instance. Set DATABASE_URL to use
Postgres instead.
"""

from .base import *
from .base import BASE_DIR, MIDDLEWARE, env

DEBUG = env.bool("DEBUG", default=False)

# WhiteNoise serves compressed, hashed static files without a separate
# web server. Must sit directly after SecurityMiddleware.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    *MIDDLEWARE[1:],
]

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# SQLite is allowed in staging only.
DATABASES = {
    "default": env.db_url(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'staging.sqlite3'}",
    ),
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Staging sits behind a proxy that terminates TLS.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Keep staging out of search results.
WAGTAIL_ENABLE_UPDATE_CHECK = False
