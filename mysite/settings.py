"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# import environ
from django.utils.translation import get_language_info
from decouple import config


# env = environ.Env()
# env.read_env()
# env.read_env('.env')

print("Testing .env loading:", os.getenv("SECRET_KEY", default="Env not loaded"))

print("DJANGO_DEBUG:", os.getenv("DJANGO_DEBUG"))
print("SECRET_KEY:", os.getenv("SECRET_KEY"))
print("TMP_XXX0:", config('TMP_XXX0', default=False, cast=bool))
print("TMP_XXX1:", config('TMP_XXX1', default=False, cast=bool))
print("TMP_XXX2:", config('TMP_XXX2', default=False, cast=bool))
print("TMP_XXX3:", config('TMP_XXX3', default=False, cast=bool))
print("TMP_XXX4:", config('TMP_XXX4', default=False, cast=bool))
print("TMP_XXX5:", config('TMP_XXX5', default=False, cast=bool))
print("TMP_XXX6:", config('TMP_XXX6', default=False, cast=bool))
print("TMP_XXX7:", config('TMP_XXX7', default=False, cast=bool))
print("TMP_XXX8:", config('TMP_XXX8', default=False, cast=bool))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# DJANGO_ENV = os.getenv("DJANGO_ENV", False)

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)
# DEBUG = env.bool('DJANGO_DEBUG', default=False)
# DEBUG = os.getenv("DJANGO_DEBUG", False)

CRON_CLASSES = [
    "ims.cron.Runspider",
    "ims.cron.VerifiedTelegram",
    "ims.cron.DeleteInvalidLinks",
    # 其他 cron 作业
]

SECURE_CROSS_ORIGIN_OPENER_POLICY = None

ALLOWED_HOSTS = ['23.95.85.37', 'imindex.fly.dev', 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'http://23.95.85.37',
    'https://imindex.fly.dev',
    'http://localhost',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
    # other folders
]

LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "verbose": {
            "format": "{levelname} [{asctime} {name}] {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            "formatter": "verbose",
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            "formatter": "verbose",
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'propagate': True,
        },
    },
}

# Application definition

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

CELERY_BROKER_URL = 'redis://redis:6379/0'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://imindex-redis-1:6379",
    }
}

CSRF_COOKIE_SECURE = False

INSTALLED_APPS = [
    "django_cron",
    "crawler",
    "common",
    "django_unicorn",
    "debug_toolbar",
    "ims.apps.ImsConfig",
    "deploy.apps.DeployConfig",
    "polls.apps.PollsConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'common.context_processors.my_custom_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "CONN_MAX_AGE": 600,
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": "db",
        "PORT": "5432",
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# if DJANGO_ENV == 'production':
#     database_config = env.db()
#     database_config['CONN_MAX_AGE'] = 600
#     DATABASES = {
#         'default': database_config
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'
# LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', 'English'),
    ('zh-hans', 'Simplified Chinese'),
    ('ja', 'Japanese'),
    ('ko', 'Korean'),
]

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True
USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
