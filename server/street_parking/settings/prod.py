import os
import string
import random

from .default import Default
from configurations import values


def get_app_key():
    APP_KEY_FILE_PTH = 'sk.txt'
    APP_KEY = None
    random.seed(16)
    if not os.path.isfile(APP_KEY_FILE_PTH):
        string_choice = "{}{}{}{}".format(string.ascii_letters, string.digits, string.punctuation, string.hexdigits)
        random_char_list = [random.SystemRandom().choice(string_choice) for i in range(50)]
        APP_KEY = ''.join(random_char_list)
        with open(APP_KEY_FILE_PTH, 'wb') as fobj:
            fobj.write(APP_KEY.encode('utf-8'))
    elif os.path.isfile(APP_KEY_FILE_PTH):
        with open(APP_KEY_FILE_PTH, 'rb') as fobj:
            APP_KEY = fobj.read().decode('utf-8')
    return APP_KEY

class Prod(Default):
    SECRET_KEY = get_app_key()

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