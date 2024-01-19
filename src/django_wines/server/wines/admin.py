from django.contrib import admin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import path
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    SolarSchedule,
)
from server.wines.models import Wine, WineTaskLog
from server.wines.services.enums import MessageKeysEnum
from server.wines.services.sender import Sender


@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    change_list_template = 'admin/custom_changelist.html'
    list_display = ('code', 'name',)
    search_fields = ('code', 'name',)

    def save_model(self, request, obj, form, change):
        """
        Переопределение метода сохранения объекта с добавлением функций отправки данных в другие сервисы.
        """
        obj.save()

        if change:
            message_key = MessageKeysEnum.UPDATE
        else:
            message_key = MessageKeysEnum.CREATE

        Sender.send_data(obj, message_key)

    def delete_model(self, request, obj):
        """
        Переопределение метода удаления объекта с добавлением функций отправки данных в другие сервисы.
        """
        Sender.send_data(obj, MessageKeysEnum.DELETE)
        obj.delete()

    def delete_queryset(self, request, queryset):
        """
        Переопределение метода удаления объектов с добавлением функций отправки данных в другие сервисы.
        """
        Sender.send_data(queryset, MessageKeysEnum.DELETE)
        queryset.delete()

    def update_data(self, request):
        """
        Метод запуска задачи обновления данных во всех сервисах по кнопке 'Обновить данные'.
        """
        qs = Wine.objects.all()
        Sender.send_data(qs, MessageKeysEnum.UPDATE_ALL)
        self.message_user(request, 'Создана задача на синхронизацию данных во всех сервисах')
        return HttpResponseRedirect('../')

    def get_urls(self):
        """Переопределение метода для добавления действия кнопки 'Обновить данные'."""
        urls = super().get_urls()
        custom_urls = [
            path('update_data/', self.update_data),
        ]
        return custom_urls + urls


@admin.register(WineTaskLog)
class WineTaskLogAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'is_coincided',)

    def has_add_permission(self, request):
        """Запрет на добавление объектов."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Запрет на удаление объектов."""
        return False

    def has_change_permission(self, request, obj=None):
        """Запрет на изменение объектов."""
        return False


admin.site.unregister(Group)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
