"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from .local import *

from pathlib import Path
import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config.SECRET_KEY

DEBUG = config.DEBUG

ALLOWED_HOSTS = ['*']

# Application definition
APPS = [
    'apps.users',
    'apps.forum',
    'apps.chat',
    'apps.statics',
]

THIRD_PARTY_APPS = [
    'jazzmin',
    'daphne',
    'channels',
]

INSTALLED_APPS = [
    *THIRD_PARTY_APPS,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *APPS,
]


# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.RedisChannelLayer',  # Use Redis as the channel layer backend
#         'CONFIG': {
#             'hosts': [('redis', 6379)],  # Adjust the host and port as per your Redis configuration
#         },
#     },
# }
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PASSWORD_RESET_TIMEOUT = 3600

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST=config.EMAIL_HOST
EMAIL_PORT=config.EMAIL_PORT
EMAIL_HOST_USER=config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=config.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS=config.EMAIL_USE_SSL

DEFAULT_FROM_EMAIL = config.EMAIL_HOST_USER
SERVER_EMAIL = config.EMAIL_HOST_USER
EMAIL_ADMIN = config.EMAIL_HOST_USER

ROOT_URLCONF = 'core.urls'

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


# WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'


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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'


USE_I18N = True

USE_TZ = True


# STATIC (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = ((os.path.join(BASE_DIR, 'static/')),)
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

# MEDIA (Images, PDF)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = '/'


LOGIN_URL = 'login'
# CSRF
CSRF_USE_SESSIONS = True
CSRF_TRUSTED_ORIGINS = ['http://16.171.6.225/',
                        'http://localhost/',
                        ]


# Cors

CORS_ALLOW_ALL_ORIGINS = True



