from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    """Команда для создания периодических задач."""

    help = 'Создание периодических задач'

    def handle(self, *args, **options):
        """Консольный вывод."""
        self.stdout.write('Начато создание периодических задач:\n')
        start = timezone.now()
        self._setup_tasks()
        self.stdout.write(
            'Периодические задачи созданы. Время: '
            f'{(timezone.now() - start).seconds / 60:.2f} мин'
        )

    @staticmethod
    def _setup_tasks():
        """Метод запуска периодических задач."""

        every_five_min_cron, _ = CrontabSchedule.objects.get_or_create(
            minute='*/5',
            timezone=settings.TIME_ZONE,
        )

        _ = PeriodicTask.objects.update_or_create(
            crontab=every_five_min_cron,
            name='Создание чейн-задачи',
            task='server.wines.tasks.create_chain_task',
        )
