"""
Django settings for the AIBridge project.
"""
from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def _env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-dev-key-change-me-in-production")

DEBUG = _env_bool("DEBUG", True)

_hosts = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost")
ALLOWED_HOSTS = [h.strip() for h in _hosts.split(",") if h.strip()]

# Allow Render/Railway/Vercel style hosts automatically when provided.
_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if _render_host and _render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_render_host)

_vercel_host = os.environ.get("VERCEL_URL")
if _vercel_host and _vercel_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_vercel_host)
if os.environ.get("VERCEL") and ".vercel.app" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(".vercel.app")

def _to_origin(host):
    if host.startswith("."):
        return f"https://*{host}"
    return f"https://{host}"


CSRF_TRUSTED_ORIGINS = [_to_origin(h) for h in ALLOWED_HOSTS if h not in ("127.0.0.1", "localhost")]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "aibridge.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_meta",
            ],
        },
    },
]

WSGI_APPLICATION = "aibridge.wsgi.application"

# Vercel's filesystem is read-only (except /tmp), so SQLite cannot persist
# there. When DATABASE_URL is set (e.g. a hosted Postgres on Vercel/Neon),
# use it; otherwise fall back to local SQLite for normal hosting/dev.
_database_url = os.environ.get("DATABASE_URL")
if _database_url:
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.parse(_database_url, conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# On Vercel, static/** is served directly by the CDN (see vercel.json) and no
# collectstatic step ever runs, so there's no manifest for WhiteNoise's
# hashing storage to read. Plain storage just emits STATIC_URL + path, which
# matches how vercel.json routes the raw source tree.
STORAGES = {
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if os.environ.get("VERCEL")
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AIBridge / Gemini configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")

SITE_NAME = "AIBridge"
SITE_TAGLINE = "Bridging People with AI"

from django.contrib.messages import constants as _messages

MESSAGE_TAGS = {
    _messages.ERROR: "danger",
}

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
