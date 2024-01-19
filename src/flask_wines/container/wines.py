from typing import List

from container.singleton import Singleton
from loguru import logger


class WineContainer(metaclass=Singleton):
    """Класс-контейнер вин."""

    wines = []

    @classmethod
    def create(cls, objs: List[dict]) -> None:
        """Метод добавления объекта в контейнер."""
        logger.info(
            'Добавление вина: {wine}'.format(wine=objs[0])
        )

        cls.wines.extend(objs)
        cls._sort()
        cls._common_logger()

    @classmethod
    def update(cls, objs: List[dict]) -> None:
        """Метод обновления объекта в контейнере."""
        update_obj = objs[0]
        logger.info(
            'Обновление данных вина: {wine}'.format(wine=update_obj)
        )

        for idx, item in enumerate(cls.wines):
            if item['code'] == update_obj['code']:
                cls.wines.pop(idx)
                cls.wines.append(update_obj)
                break

        cls._sort()
        cls._common_logger()

    @classmethod
    def update_all(cls, objs: List[dict]) -> None:
        """Метод обновления всех вин в контейнере."""
        logger.info(
            'Обновление всего списка вин'
        )

        cls.wines = objs
        cls._sort()
        cls._common_logger()

    @classmethod
    def delete(cls, objs: List[dict]) -> None:
        """Метод удаления вина из контейнера."""
        for obj in objs:
            logger.info(
                'Удаление вина: {wine}'.format(wine=obj)
            )

            try:
                idx = cls.wines.index(obj)
                cls.wines.pop(idx)
            except ValueError:
                logger.warning(
                    'Вино отсутствует в контейнере: {wine}'.format(wine=obj)
                )

        cls._common_logger()

    @classmethod
    def get_next(cls, objs: List[dict]) -> dict:
        """Получение следующего по списку вина."""
        idx = cls.wines.index(objs[0])
        return cls.wines[idx + 1]

    @classmethod
    def _sort(cls) -> None:
        """Метод сортировки списка вин по коду."""
        cls.wines.sort(key=lambda item: item['code'])

    @classmethod
    def _common_logger(cls) -> None:
        """Метод логирования данных в контейнере после операции изменения."""
        logger.info(
            'Список вин: {wines}'.format(wines=cls.wines)
        )


wines = WineContainer()
