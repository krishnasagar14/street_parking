import os

from .default import Default
from configurations import values

class Prod(Default):
    SECRET_KEY = ''

    DEBUG = values.BooleanValue(False)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'street_parking',
            'OPTIONS': {
                'init_command': 'SET sql_mode="STRICT_TRANS_TABLES", innodb_strict_mode=1;',
                'charset': 'utf8mb4',
            },
            'USER': 'street_parking',
            'PASSWORD': 'street_parking',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }