"""
Base settings shared by every environment.

Environment-specific modules (dev/staging/production) import everything from
here and override only what differs. No secrets live in this file - they are
read from the environment via django-environ. See ``.env.example``.
"""

from pathlib import Path

import environ

# endeavours/settings/base.py -> endeavours/settings -> endeavours -> <repo root>
PROJECT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = PROJECT_DIR.parent

env = environ.Env()

# Read a local .env file when present. Deployed environments are expected to
# provide real environment variables instead.
_env_file = BASE_DIR / ".env"
if _env_file.exists():
    env.read_env(_env_file)


# Application definition

INSTALLED_APPS = [
    # Project apps
    "apps.core",
    "apps.home",
    "apps.pages",
    "search",
    # Wagtail
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    # Third party
    "modelcluster",
    "taggit",
    "django_filters",
    "django_htmx",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "endeavours.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            PROJECT_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "apps.core.context_processors.navigation",
            ],
        },
    },
]

WSGI_APPLICATION = "endeavours.wsgi.application"


# Database
# Every environment reads DATABASE_URL; dev and production default to Postgres.

DATABASES = {
    "default": env.db_url(
        "DATABASE_URL",
        default="postgres://postgres:postgres@localhost:5432/endeavours",
    ),
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Password validation

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


# Internationalization

LANGUAGE_CODE = "en-us"
TIME_ZONE = env.str("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True


# Static files and media

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    PROJECT_DIR / "static",
]

STATIC_ROOT = env.path("STATIC_ROOT", default=BASE_DIR / "staticfiles")
STATIC_URL = "/static/"


MEDIA_ROOT = env.path("MEDIA_ROOT", default=BASE_DIR / "media")
MEDIA_URL = "/media/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Complex page models can exceed Django's default form field limit inside the
# Wagtail page editor.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000


# Email

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="noreply@endeavours.example")


# Wagtail

WAGTAIL_SITE_NAME = "Endeavours"

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL used for full URLs in the admin (notification emails, previews).
# No '/admin' suffix and no trailing slash.
WAGTAILADMIN_BASE_URL = env.str("WAGTAILADMIN_BASE_URL", default="http://localhost:8000")

WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]

WAGTAILDOCS_MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

WAGTAILIMAGES_IMAGE_MODEL = "core.CustomImage"

# Editors should not be able to leave a page without a title in menus.
WAGTAIL_ALLOW_UNICODE_SLUGS = False
