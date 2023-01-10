import os
import dj_database_url
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['web-production-db1d.up.railway.app']

DATABASES = {
    'default': dj_database_url.config()
}

REDIS_URL = os.environ['REDIS_URL']

# (command) celery -A the_pillar worker --loglevel=info
# "--loglevel=info" is only used in development
CELERY_BROKER_URL = REDIS_URL

# (BGtasks monitoring tool/command) celery -A the_pillar flower
# url: localhost:5555
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
# EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
# EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
# EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']

CSRF_TRUSTED_ORIGINS = ['https://web-production-db1d.up.railway.app']

# AWS s3 configurations
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

DEFAULT_FILE_STORAGE = 'the_pillar.settings.storage_backends.MediaStorage'
MEDIA_URL = f'{AWS_S3_CUSTOM_DOMAIN}/media/'

# To enable uploading of the same file without overwriting previous files
# AWS_S3_FILE_OVERWRITE = False

# Forgot password
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
