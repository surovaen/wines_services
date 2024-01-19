import uuid

from django.conf import settings
from loguru import logger
from server import celery_app
from server.wines.models import WineTaskLog
from server.wines.services.enums import MessageKeysEnum
from server.wines.services.sender import Sender
from server.wines.utils import get_next_wine, get_random_wine


@celery_app.task()
def create_chain_task() -> None:
    """Формирование чейн-задачи для сервисов."""
    wine = get_random_wine()

    if wine:
        log_uuid = uuid.uuid4()
        logger.info(
            'Отправка вина {wine} для чейн-задачи {log}'.format(
                wine=wine,
                log=log_uuid,
            ),
        )

        log = WineTaskLog(
            uuid=log_uuid,
            sent_wine=wine.code,
        )

        Sender.send_chain_data(
            objs=wine,
            key=MessageKeysEnum.CHAIN_TASK,
            log_uuid=str(log_uuid),
        )

        for _ in range(settings.SERVICES_COUNT):
            wine = get_next_wine(wine)

        log.expected_wine = wine.code
        log.save()

    else:
        logger.info(
            'Список вин недостаточен для формирования чейн-задачи',
        )


@celery_app.task()
def process_chain_task(body: dict) -> None:
    """Обработка результата выполнения чейн-задачи."""
    wine = body.get('data')[0]
    wine_code = wine.get('code')
    log_uuid = body.get('log_uuid')

    logger.info(
        'Обработка вина {wine}, полученного в результате выполнения чейн-задачи {log}'.format(
            wine=wine,
            log=log_uuid,
        )
    )

    log = WineTaskLog.objects.filter(
        uuid=log_uuid,
    ).first()
    log.received_wine = wine_code
    log.save()


@celery_app.task()
def error_handler(request, exc, traceback):
    """Обработка ошибки выполнения задачи."""
    task = request.get('task')

    logger.error(
        'Ошибка выполнения задачи "{task}"\n {exc}: {trace}'.format(
            task=task,
            exc=exc,
            trace=traceback,
        ),
    )
