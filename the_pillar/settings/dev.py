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
        'TIMEOUT': 1,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST = 'localhost'  # smtp4dev
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda request: True
# }

MEDIA_URL = '/media/'
