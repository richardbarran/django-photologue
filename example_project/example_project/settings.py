# Global settings for photologue example project.

import os
import sys
from photologue import PHOTOLOGUE_APP_DIR

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
USE_TZ = True

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

TEMPLATE_DIRS = (
    os.path.join(TOP_FOLDER, 'example_project/templates'),
    os.path.join(PHOTOLOGUE_APP_DIR, 'contrib/bootstrap/templates'),
    PHOTOLOGUE_APP_DIR
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

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Note: added sitemaps to the INSTALLED_APPS just so that unit tests run,
    # but not actually added a sitemap in urls.py.
    'django.contrib.sitemaps',
    'photologue',
    'sortedm2m',
    'south',
    'example_project',
]

# LOGGING CONFIGURATION
# A logging configuration that writes log messages to the console.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    # Formatting of messages.
    'formatters': {
        # Don't need to show the time when logging to console.
        'console': {
            'format': '%(levelname)s %(name)s.%(funcName)s (%(lineno)d) %(message)s'
        }
    },
    # The handlers decide what we should do with a logging message - do we email
    # it, ditch it, or write it to a file?
    'handlers': {
        # Writing to console. Use only in dev.
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        # Send logs to /dev/null.
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
    },
    # Loggers decide what is logged.
    'loggers': {
        '': {
            # Default (suitable for dev) is to log to console.
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'photologue': {
            # Default (suitable for dev) is to log to console.
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # logging of SQL statements. Default is to ditch them (send them to
        # null). Note that this logger only works if DEBUG = True.
        'django.db.backends': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# Don't display logging messages to console during unit test runs.
if len(sys.argv) > 1 and sys.argv[1] == 'test':
    LOGGING['loggers']['']['handlers'] = ['null']
    LOGGING['loggers']['photologue']['handlers'] = ['null']

SOUTH_TESTS_MIGRATE = False
