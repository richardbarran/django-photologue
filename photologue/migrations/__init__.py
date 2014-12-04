"""
Migrations used by Django 1.7.
South migrations can be found in the ``south_migrations`` package.
"""

# Code from http://treyhunner.com/2014/03/migrating-to-django-1-dot-7/

SOUTH_ERROR_MESSAGE = """\n
If you're on Django 1.6 (or earlier), you'll need to set SOUTH_MIGRATION_MODULES.
Please refer to the installation docs.
"""

# Ensure the user is not using Django 1.6 or below with South
try:
    from django.db import migrations
except ImportError:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(SOUTH_ERROR_MESSAGE)
