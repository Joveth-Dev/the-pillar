release: python manage.py migrate
web: gunicorn the_pillar.wsgi --log-file -
worker: celery -A the_pillar worker