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

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env_str('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,
        },
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "_project_/static/",
]

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
