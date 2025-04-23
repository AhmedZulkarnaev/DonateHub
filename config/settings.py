from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv

# ==== Базовые настройки проекта ====

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)

SECRET_KEY = os.getenv("SECRET_KEY", "key")
DEBUG = os.getenv("DEBUG", "").lower() == "true"
ALLOWED_HOSTS = []

# ==== Установленные приложения ====

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "djoser",
    "drf_yasg",
    # Local apps
    "donations.apps.DonationsConfig",
]

# ==== Middleware ====

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==== URL конфигурация ====

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ==== База данных ====

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# ==== Валидация паролей ====

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==== Локализация ====

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ==== Статические файлы ====

STATIC_URL = "static/"

# ==== Настройки DRF ====

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

# ==== Настройки DJOSER ====

DJOSER = {
    "USER_CREATE_PASSWORD_RETYPE": True,
}

# ==== JWT ====

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# ==== Кэш ====

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        "TIMEOUT": 60 * 5,
        "OPTIONS": {"MAX_ENTRIES": 1000},
    }
}

# ==== Swagger ====

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT авторизация. Пример: "Bearer {token}"',
        }
    },
    "USE_SESSION_AUTH": False,
    "JSON_EDITOR": True,
}

# ==== Celery ====

CELERY_BROKER_URL = "redis://redis:6379/0"

# ==== Email ====

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "ahmedzulkarnaev9500@gmail.com"
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ==== Поля по умолчанию ====

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
