from django.db import models


class Wine(models.Model):
    """Модель вин."""

    code = models.AutoField(
        'Код',
        primary_key=True,
    )
    name = models.CharField(
        'Наименование',
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = 'Вино'
        verbose_name_plural = 'Вина'
        ordering = ('code',)

    def __str__(self) -> str:
        return f'{self.name}'


class WineTaskLog(models.Model):
    """Модель лога выполнения чейн-задачи."""

    uuid = models.UUIDField(
        'Идентификатор лога',
        max_length=255,
    )
    created_at = models.DateTimeField(
        'Дата и время запуска задачи',
        auto_now_add=True,
    )
    sent_wine = models.PositiveIntegerField(
        'Код отправленного вина',
        null=True,
    )
    expected_wine = models.PositiveIntegerField(
        'Код ожидаемого вина',
        null=True,
    )
    received_wine = models.PositiveIntegerField(
        'Код полученного вина',
        null=True,
    )
    is_coincided = models.BooleanField(
        'Совпало',
        default=False,
    )

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи чейн-задач'
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.created_at} - {self.uuid}'

    def save(self, *args, **kwargs):
        """Добавление логики установки признака 'Совпало' при сохранении объекта."""
        if self.expected_wine == self.received_wine:
            self.is_coincided = True

        return super().save(*args, **kwargs)
