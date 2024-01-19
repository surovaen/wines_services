import random
from typing import Optional

from server import settings
from server.wines.models import Wine


def get_random_wine() -> Optional[Wine]:
    """Получение случайного объекта модели."""
    qs = Wine.objects.all()

    if len(qs) > settings.SERVICES_COUNT:
        random_idx = random.randint(0, len(qs) - settings.SERVICES_COUNT)
        return qs[random_idx]

    return None


def get_next_wine(obj: Wine) -> Wine:
    """Получение следующего вина по коду из БД."""
    wine = Wine.objects.filter(
        code__gt=obj.code,
    ).order_by('code').first()

    return wine
