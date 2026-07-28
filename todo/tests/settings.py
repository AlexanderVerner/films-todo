"""
Test-only Django settings.

Only test-specific values live here: everything shared with the
production settings (``_project_/settings.py``) lives in
``_project_/settings_base.py``.
"""
from envjson import env_str

from _project_.settings_base import *  # noqa: F401,F403

# Hardcoded, non-secret key: tests never talk to a real deployment so this
# does not need to come from the environment.
SECRET_KEY = 'eiCeiSh2aa01xaiGha0paig4isai5oon0rahnaethohWi2ophoophier8h'

DEBUG = True

INSTALLED_APPS = BASE_INSTALLED_APPS + [
    'constance.backends.database',
    'rest_framework',
]

# For tests: use separate database to avoid overwriting production data
TEST_POSTGRES_DATABASE_NAME = env_str("TEST_POSTGRES_DATABASE_NAME", f"{POSTGRES_DATABASE_NAME}_test")

DATABASES = build_databases_config(TEST_POSTGRES_DATABASE_NAME)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
