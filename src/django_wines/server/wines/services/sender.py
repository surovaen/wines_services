from typing import Union

from celery import chain, signature
from django.conf import settings
from django.db.models import QuerySet
from loguru import logger
from server import celery_app
from server.wines.models import Wine
from server.wines.services.enums import MessageKeysEnum
from server.wines.services.message import Message


class Sender:
    """Класс отправки задач."""

    app = celery_app

    @classmethod
    def send_data(cls, *args, **kwargs) -> None:
        """Отправка сообщения об изменении данных в другие сервисы."""
        msg = cls._create_message(*args, **kwargs)

        logger.info(
            'Отправка сообщения во все сервисы: {msg}'.format(msg=msg),
        )
        flask_task = cls.app.signature(
            'tasks.tasks.process_wine_data',
            kwargs={'body': msg},
        ).set(
            link_error=signature(
                'server.wines.tasks.error_handler',
            ),
        )
        flask_task.apply_async(
            exchange='wines',
            routing_key='flask_wine_data_*',
        )

    @classmethod
    def send_chain_data(cls, *args, **kwargs) -> None:
        """Отправка сообщения для чейн-задачи."""
        msg = cls._create_message(*args, **kwargs)
        flask_queue = settings.FLASK_DEFAULT_QUEUE
        tasks_list = [
            signature(
                'tasks.tasks.process_chain_task',
                queue=flask_queue.format(num=1),
                args=[msg],
            ),
        ]

        if settings.SERVICES_COUNT > 1:
            tasks_list.extend(
                [
                    signature(
                        'tasks.tasks.process_chain_task',
                        queue=flask_queue.format(num=i),
                    ) for i in range(2, settings.SERVICES_COUNT + 1)
                ],
            )

        tasks_list.append(
            signature(
                'server.wines.tasks.process_chain_task',
                queue='django_default',
            ),
        )
        chained_task = chain(*tasks_list).set(
            link_error=signature(
                'server.wines.tasks.error_handler',
            ),
        )
        chained_task()

    @classmethod
    def _create_message(
            cls,
            objs: Union[Wine, QuerySet[Wine]],
            key: MessageKeysEnum,
            log_uuid: str = None,
    ) -> dict:
        """Метод формирования сообщения для сервисов."""
        if isinstance(objs, Wine):
            objs = [objs]

        msg = Message.create(
            objs=objs,
            message_key=key,
            log_uuid=log_uuid,
        )

        return msg
