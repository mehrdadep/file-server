"""
Django settings for file_server project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('FILE_SERVER_SECRET_KEY',
                       'h7no2l47ur9jx^)2b-mlp@_hckf#*yqvwtbgtys*&zlc=yp(@u')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv(
    'FILE_SERVER_DEBUG_MODE',
    'True',
) == 'True' else False
ALLOWED_HOSTS = [
    e.strip() for e in os.getenv("FILE_SERVER_ALLOWED_HOSTS").split(',')
]

# Application definition

INSTALLED_APPS = [
    # Django Modules.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Modules.
    'rest_framework',

    # File server Applications.
    'file_server.apps.files.apps.FilesConfig',

    # Health check apps
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'file_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'file_server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('FILE_SERVER_DATABASES_NAME'),
        'USER': os.getenv('FILE_SERVER_DATABASES_USER'),
        'PASSWORD': os.getenv('FILE_SERVER_DATABASES_PASSWORD'),
        'HOST': os.getenv('FILE_SERVER_DATABASES_HOST'),
        'PORT': os.getenv('FILE_SERVER_DATABASES_PORT', 5432),
        'TEST': {
            'NAME': os.getenv('FILE_SERVER_DATABASES_TEST_NAME'),
        },
    },
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{os.getenv('FILE_SERVER_REDIS_HOST')}:"
                    f"{os.getenv('FILE_SERVER_REDIS_PORT')}/"
                    f"{os.getenv('FILE_SERVER_CACHE_DATABASE')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": os.getenv('FILE_SERVER_CACHE_PREFIX')
    }
}
# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%s.%f',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.MultiPartParser'
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LANGUAGES = (
    ('fa', 'Farsi'),
    ('en', 'English'),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

MEDIA_URL = os.getenv('FILE_SERVER_MEDIA_URL', '/files/')
MEDIA_ROOT = os.getenv('FILE_SERVER_MEDIA_ROOT', '/var/share/file_server/')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = os.getenv('FILE_SERVER_STATIC_URL', '/static/')

STATICFILE_SERVER_DIRS = (
    os.path.join(BASE_DIR, os.getenv(
        'FILE_SERVER_STATIC_DIRS',
        'staticfiles',
    )),
)

STATIC_ROOT = os.path.join(
    BASE_DIR, os.getenv(
        'FILE_SERVER_STATIC_ROOT',
        'static',
    ),
)

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 50000000
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
# MAX_UPLOAD_SIZE represented in bytes
FILE_SERVER = {
    'CACHE_EXPIRY': int(os.getenv(
        'FILE_SERVER_CACHE_EXPIRY',
        86400,
    )),
    'MAX_UPLOAD_SIZE': os.getenv(
        'FILE_SERVER_MAX_UPLOAD_SIZE',
        50000000,
    ),
}
