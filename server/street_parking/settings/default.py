"""
Django settings for street_parking project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import platform

from configurations import Configuration, values
from corsheaders.defaults import default_headers

LOG_DIR_PATH = None
PRODUCT_PATH = None
PRODUCT_NAME = 'StreetParking'
LOG_DIR_NAME = 'Logs'
STATIC_DIR_NAME = 'Static'
if platform.system() == 'Windows':
    app_data_path = os.getenv('APPDATA')
    PRODUCT_PATH = "{}\{}".format(app_data_path, PRODUCT_NAME)
elif platform.system() == 'Linux':
    PRODUCT_PATH = '/var/log/{}/'.format(PRODUCT_NAME)
else:
    PRODUCT_PATH = './{}/'.format(PRODUCT_NAME)

LOG_DIR_PATH = os.path.join(PRODUCT_PATH, LOG_DIR_NAME)

if not os.path.isdir(LOG_DIR_PATH):
    os.mkdir(LOG_DIR_PATH, mode=0x577)

class Default(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'd^2r)gg^^0oxj8$-6)3&l7s(agk8fea^p(3-i+(f2rbf_^ewbq'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = []


    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'rest_framework',
        'corsheaders',
        'drf_yasg',
        'django_filters',
        'django_extensions',

        'common',
        'core',
        'apps.user',
        'apps.authentication',
        'apps.reservations',
        'apps.parkSpot',
    ]

    AUTH_USER_MODEL = 'user.User'

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',

        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'street_parking.urls'

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

    WSGI_APPLICATION = 'street_parking.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/2.1/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/2.1/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.1/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(PRODUCT_PATH, STATIC_DIR_NAME)

    # CORS support

    CORS_ORIGIN_ALLOW_ALL = values.BooleanValue(True)
    CORS_ALLOW_HEADERS = default_headers + (
        'Access-Control-Allow-Origin',
    )

    # Product settings

    PRODUCT_NAME = PRODUCT_NAME
    APPLICATION_NAME = PRODUCT_NAME + 'APIs'
    VERSION = 'v19.02.24'
    DESCRIPTION = 'Street parking reservation service'
    CONTACT = 'pagesagar@gmail.com'
    BASE_URL = 'http://localhost:8000'

    # django Logging config

    LOGGING = {
        'version': 1.0,
        'handlers': {
            'access_log': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(LOG_DIR_PATH, 'access.log'),
                'formatter': 'prod',
            },
            'error_log': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': os.path.join(LOG_DIR_PATH, 'error.log'),
                'formatter': 'prod',
            }
        },
        'formatters': {
            'prod': {
                'format': '{levelname} - {asctime} - {process:d} - {thread:d} - {filename} - {lineno} - {message}',
                'style': '{'
            }
        },
        'disable_existing_loggers': values.BooleanValue(False),
        'loggers': {
            'django': {
                'handlers': ['access_log', 'error_log'],
                'level': 'DEBUG',
                'propagate': values.BooleanValue(True),
            }
        },
    }

    # DRF configs
    REST_FRAMEWORK = {
        'DEFAULT_FILTER_BACKENDS': (
            'django_filters.rest_framework.DjangoFilterBackend',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.JSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'apps.authentication.authSchemes.BearerAuthentication',
        ),
        'DEFAULT_THROTTLE_CLASSES': (
            'rest_framework.throttling.AnonRateThrottle',
            'rest_framework.throttling.UserRateThrottle',
        ),
        'EXCEPTION_HANDLER': 'core.exceptionsHandlers.ApplnExceptionHandler',
    }