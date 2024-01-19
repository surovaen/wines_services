from decouple import config


class Config:
    """Класс конфигурации."""

    RABBIT_HOST = config('RABBIT_HOST', default='localhost')
    RABBIT_PORT = config('RABBIT_PORT', default=5672, cast=int)
    RABBIT_URL = f'amqp://{RABBIT_HOST}:{RABBIT_PORT}'

    SERVICE_NUMBER = config('SERVICE_NUMBER', default=1, cast=int)
    DEFAULT_QUEUE = 'flask_default_{num}'.format(num=SERVICE_NUMBER)
    DATA_QUEUE = 'flask_wine_data_{num}'.format(num=SERVICE_NUMBER)
