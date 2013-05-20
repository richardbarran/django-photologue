# Global settings for photologue example project.

import sys
import os

DEBUG = TEMPLATE_DEBUG = True

# Top level folder - the one created by the startproject command.
TOP_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ADMINS = ()

MANAGERS = ADMINS

# Default dev database is Sqlite. In production I use postgres.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(TOP_FOLDER, 'database.sql3')
    }
}

TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
# TODO: setting this to True in Django 1.4 causes runtime warnings, when 1.4
# is end-of-lined in 2014 we can change this setting to True.
USE_TZ = False

MEDIA_ROOT = os.path.join(TOP_FOLDER, 'public', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(TOP_FOLDER, 'public', 'static')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(TOP_FOLDER, 'example_project/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3p0f5q)l$=gt++#z0inpfh%bm_ujl6(-yogbzw2)(xea48@70d'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'example_project.urls'

from photologue import PHOTOLOGUE_TEMPLATE_DIR
TEMPLATE_DIRS = (
    os.path.join(TOP_FOLDER, 'example_project/templates'),
    PHOTOLOGUE_TEMPLATE_DIR
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

FIXTURE_DIRS = (
    os.path.join(TOP_FOLDER, 'example_project/fixtures'),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'photologue',
    'example_project',
]

if sys.version_info <= (3, 0):
    # South does not support Python 3
    INSTALLED_APPS += ['south']


SOUTH_TESTS_MIGRATE = False

