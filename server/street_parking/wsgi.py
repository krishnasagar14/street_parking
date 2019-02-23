"""
WSGI config for street_parking project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

#from django.core.wsgi import get_wsgi_application
# NOTE: entry point changed to django_configurations
from configurations.wsgi import get_wsgi_application

config = os.getenv('ENVIRONMENT', 'local').lower()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'street_parking.settings.{}'.format(config))
os.environ.setdefault('DJANGO_CONFIGURATION', config.title())

application = get_wsgi_application()
