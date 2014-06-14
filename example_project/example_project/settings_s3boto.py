# S3Boto storage settings for photologue example project.

import os

DEFAULT_FILE_STORAGE = 'example_project.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'example_project.s3utils.StaticS3BotoStorage'

try:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
except KeyError:
    raise KeyError('Need to define AWS environment variables: ' + \
        'AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_STORAGE_BUCKET_NAME')
AWS_REGION = os.environ.get('AWS_REGION', '')
if AWS_REGION != '':
    AWS_REGION = '-' + AWS_REGION

# Default Django Storage API behavior - don't overwrite files with same name
AWS_S3_FILE_OVERWRITE = False

MEDIA_ROOT = '/media/'
MEDIA_URL = 'https://%s.s3%s.amazonaws.com/media/' \
    % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)

STATIC_ROOT = '/static/'
STATIC_URL = 'https://%s.s3%s.amazonaws.com/static/' \
    % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
