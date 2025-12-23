"""The signal extentions for app $PATH_TO_APP"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from apps.my_workflows.models import Task


_task_state_cache = {}


@receiver(pre_save, sender=Task)
def capture_task_state(sender, instance, **kwargs):
    """
    Запоминаем состояние задачи ДО сохранения.
    """
    if instance.pk:  # Только для существующих записей
        try:
            old_instance = Task.objects.get(pk=instance.pk)
            print(old_instance)
            _task_state_cache[instance.pk] = {
                'instance': old_instance,
                'fields': {
                    'status': old_instance.status
                }
            }
        except Task.DoesNotExist:
            pass


@receiver(post_save, sender=Task)
def logging_task_actions(sender, instance, created, **kwargs):
    """
    Обрабатывает создание и обновление с использованием кеша.
    """
    from apps.my_workflows.handlers import logging_task_actions_handler

    if created:
        logging_task_actions_handler(task_instance=instance, action='created')

    else:
        # Достаем старое состояние из кеша
        old_data = _task_state_cache.pop(instance.pk, None)
        print(old_data)
        if old_data:
            old_instance = old_data['instance']
            old_fields = old_data['fields']

            # Быстрое сравнение полей
            changed_fields = {}

            # Сравниваем только нужные поля
            if old_fields['status'] != instance.status:
                changed_fields['status'] = {
                    'from': old_fields['status'],
                    'to': instance.status
                }

            # Вызываем обработчик если есть изменения
            if changed_fields:
                logging_task_actions_handler(
                    task_instance=instance,
                    action='updated',
                    old_instance=old_instance,
                    changed_fields=changed_fields
                )
