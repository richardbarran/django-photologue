# S3Boto storage settings for photologue example project.

import os

DEFAULT_FILE_STORAGE = 'example_project.example_storages.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'example_project.example_storages.s3utils.StaticS3BotoStorage'

try:
    # If you want to test the example_project with S3, you'll have to configure the
    # environment variables as specified below.
    # (Secret keys are stored in environment variables for security - you don't want to
    # accidentally commit and push them to a public repository).
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
except KeyError:
    raise KeyError('Need to define AWS environment variables: ' +
                   'AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_STORAGE_BUCKET_NAME')

# Default Django Storage API behavior - don't overwrite files with same name
AWS_S3_FILE_OVERWRITE = False

MEDIA_ROOT = '/media/'
MEDIA_URL = 'http://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME

STATIC_ROOT = '/static/'
STATIC_URL = 'http://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
