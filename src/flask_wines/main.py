from celery_app import celery_init_app
from config import Config
from flask import Flask
from kombu import Exchange, Queue


app = Flask(__name__)
app.config.from_object(Config())

app.config.from_mapping(
    CELERY=dict(
        broker_url=app.config['RABBIT_URL'],
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)

wine_exchange = Exchange('wines', type='fanout')
default_exchange = Exchange('flask_default', type='direct')

celery_app.conf.task_queues = (
    Queue(app.config['DATA_QUEUE'], wine_exchange, routing_key=app.config['DATA_QUEUE']),
    Queue(app.config['DEFAULT_QUEUE'], default_exchange, routing_key=app.config['DEFAULT_QUEUE']),
)
