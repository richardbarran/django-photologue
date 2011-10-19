from tempfile import mkdtemp

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

ROOT_URLCONF = 'photologue.urls'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'photologue',
)

MEDIA_ROOT = mkdtemp()
