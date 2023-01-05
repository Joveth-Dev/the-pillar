import config
from .common import *

# TESTING REVERT WHEN DONE
DEBUG = True  # Should be True

SECRET_KEY = 'django-insecure-2ho(1l9=@8o1ml*66l=0xb+w1(s1*6v-z@^+g&t$^^p_zi6x($'

# TO DOCKERIZE
# change...
# localhost - mysql
# CELERY_BROKER_URL domain - redis
# CACHES' LOCATION domain - redis
# EMAIL_HOST - smtp4dev


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'the_pillar',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '@Sql09518342134',
    }
}

# (command) celery -A the_pillar worker --loglevel=info
# "--loglevel=info" is only used in development
CELERY_BROKER_URL = 'redis://localhost:6379/1'  # redis

# (BGtasks monitoring tool/command) celery -A the_pillar flower
# url: localhost:5555
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",  # redis
        'TIMEOUT': 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# EMAIL_HOST = 'localhost'  # smtp4dev
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 2525

# FOR FORGOT PASSOWORD FEATURE
# DOMAIN = '127.0.0.1:5500'
EMAIL_HOST_USER = config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
# PASSWORD_RESET_CONFIRM_URL = '/password/reset/confirm/{uid}/{token}',

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda request: True
# }

CUSTOM_DOMAIN_URL = 'http://127.0.0.1:8800'

MEDIA_URL = '/media/'

DATA_UPLOAD_MAX_MEMORY_SIZE = 15728640  # 15MiB
