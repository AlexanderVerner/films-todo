"""
Shared Django settings for the ``films-todo`` project.

This module holds everything that is identical between the production
settings (``_project_/settings.py``) and the test settings
(``todo/tests/settings.py``): installed apps shared by both environments,
middleware, templates, database connection parameters, password
validation, i18n, and logging.

Neither ``_project_/settings.py`` nor ``todo/tests/settings.py`` should be
used directly as a Django settings module on its own -- they both build on
top of this file via ``from _project_.settings_base import *`` and only
override the handful of values that legitimately differ between prod and
tests (SECRET_KEY, DEBUG, INSTALLED_APPS extras, DATABASES name, STATIC_*).
"""
import os
from os.path import dirname, join
from pathlib import Path
from envjson import env_str, env_json, env_json_int, env_json_bool

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = dirname(__file__)


ALLOWED_HOSTS = env_json("ALLOWED_HOSTS")


# Application definition
# Apps shared by every environment. Environment-specific apps (e.g. the
# ``rest_framework`` API or test-only apps such as ``constance``) are
# appended on top of this list by the environment-specific settings module.

BASE_INSTALLED_APPS = [
    'todo.apps.TodoConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '_project_.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [
            join(PROJECT_DIR, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '_project_.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

POSTGRES_HOST = env_str("POSTGRES_HOST")
POSTGRES_PORT = env_json_int("POSTGRES_PORT", 5432)
POSTGRES_USER = env_str("POSTGRES_USER")
POSTGRES_PASSWORD = env_str("POSTGRES_PASSWORD")
POSTGRES_DATABASE_NAME = env_str("POSTGRES_DATABASE_NAME")
POSTGRES_USE_TLS = env_json_bool("POSTGRES_USE_TLS", False)

POSTGRES_SSL_MODE = "require" if POSTGRES_USE_TLS else None


def build_databases_config(database_name):
    """Build the Django ``DATABASES`` dict for the given database name.

    Every environment connects to the same Postgres server/credentials --
    only the database name differs (e.g. prod vs. the ``_test`` suffixed
    database used by the test settings).
    """
    return {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": database_name,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": POSTGRES_HOST,
            "PORT": POSTGRES_PORT,
            "OPTIONS": {"sslmode": POSTGRES_SSL_MODE},
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
# https://docs.djangoproject.com/en/4.1/topics/logging/
# Shared so that what is exercised in tests matches what runs in prod.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
        },
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {funcName}:{lineno} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'json',
            'level': 'INFO',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
        },
    },
    'loggers': {
        'todo': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
