import enum


class MessageKeysEnum(enum.Enum):
    """Класс перечислений типов сообщений."""

    UPDATE = 'update'
    DELETE = 'delete'
    CREATE = 'create'
    UPDATE_ALL = 'update_all'
    CHAIN_TASK = 'chain_task'
