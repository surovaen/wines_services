from typing import List, Union

from django.db.models import QuerySet
from server.wines.models import Wine
from server.wines.services.enums import MessageKeysEnum


class Message:
    """Класс формирования сообщения."""

    @classmethod
    def create(
            cls,
            objs: Union[List[Wine], QuerySet[Wine]],
            message_key: MessageKeysEnum,
            log_uuid: str = None,
    ) -> dict:
        """Метод создания сообщения по измененным данным с типом операции."""
        msg = {
            'key': message_key.value,
            'data': [
                {'code': obj.code, 'name': obj.name} for obj in objs
            ],
        }

        if log_uuid:
            msg['log_uuid'] = log_uuid

        return msg
