# Copyright 2012 django-htmlmin authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'photologue.db',
    },
}

INSTALLED_APPS = (
    'photologue',
    'django_nose',
)

MEDIA_ROOT = os.path.join(BASEDIR, 'media')

ROOT_URLCONF = 'photologue.urls'

TEMPLATE_DIRS = (
    os.path.join(BASEDIR, 'templates')
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SECRET_KEY = 'secret'
