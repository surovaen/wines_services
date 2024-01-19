from container.wines import wines
from loguru import logger
from main import celery_app
from tasks.enums import TASK_ACTIONS_MAP


@celery_app.task()
def process_wine_data(body: dict) -> None:
    """Задача обработки изменения данных о винах в главном сервисе."""
    TASK_ACTIONS_MAP[body['key']](body['data'])


@celery_app.task()
def process_chain_task(body: dict) -> dict:
    """Задача обработки чейн-задачи."""
    wine = body['data']

    logger.info(
        'Получено вино {wine} для выполнения чейн-задачи'.format(
            wine=wine,
        ),
    )

    body.update(
        {
            'data': [
                wines.get_next(wine),
            ]
        }
    )
    return body
