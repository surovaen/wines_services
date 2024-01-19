import enum

from container.wines import wines


class MessageKeysEnum(enum.Enum):
    """Класс перечислений типов сообщений."""

    UPDATE = 'update'
    DELETE = 'delete'
    CREATE = 'create'
    UPDATE_ALL = 'update_all'
    CHAIN_TASK = 'chain_task'


TASK_ACTIONS_MAP = {
    MessageKeysEnum.UPDATE_ALL.value: wines.update_all,
    MessageKeysEnum.UPDATE.value: wines.update,
    MessageKeysEnum.DELETE.value: wines.delete,
    MessageKeysEnum.CREATE.value: wines.create,
}
