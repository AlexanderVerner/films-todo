from os.path import dirname, join
from pathlib import Path
from envjson import env_str, env_json, env_json_int, env_json_bool

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = dirname(__file__)


SECRET_KEY = 'eiCeiSh2aa01xaiGha0paig4isai5oon0rahnaethohWi2ophoophier8h'

DEBUG = True

ALLOWED_HOSTS = env_json("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    'todo.apps.TodoConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'constance.backends.database',
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": POSTGRES_DATABASE_NAME,
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
