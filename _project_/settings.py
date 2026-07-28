"""
Production Django settings.

Only prod-specific values live here: everything shared with the test
settings (``todo/tests/settings.py``) lives in ``_project_/settings_base.py``.
"""
import os

from envjson import env_str, env_json_bool

from _project_.settings_base import *  # noqa: F401,F403

SECRET_KEY = env_str("SECRET_KEY", "dev-insecure-secret-key-only-for-local-development")

DEBUG = env_json_bool("DEBUG", False)

INSTALLED_APPS = BASE_INSTALLED_APPS + [
    'rest_framework',
]

DATABASES = build_databases_config(POSTGRES_DATABASE_NAME)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "_project_/static/",
]

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
