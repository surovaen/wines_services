import os

from celery import Celery
from kombu import Exchange, Queue


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

celery_app = Celery('server')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
celery_app.conf.timezone = 'UTC'

default_exchange = Exchange('django_default', type='direct')

celery_app.conf.task_queues = (
    Queue('django_default', default_exchange, routing_key='django_default'),
)
celery_app.conf.task_default_queue = 'django_default'
