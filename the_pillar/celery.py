import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_pillar.settings.dev')

celery = Celery('the_pillar')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
