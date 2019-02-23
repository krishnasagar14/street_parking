#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    config = os.getenv('ENVIRONMENT', 'local').lower()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'street_parking.settings.{}'.format(config))
    os.environ.setdefault('DJANGO_CONFIGURATION', config.title())
    try:
        #from django.core.management import execute_from_command_line
        # NOTE: entry point changed to django_configurations
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
