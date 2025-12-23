"""The handler extentions for app $PATH_TO_APP"""
from django.utils import timezone
from django.db import transaction
from apps.my_workflows.models import CycleTime


PHASE_CHOICES = [
    ('lead_time', 'Полное время (от создания до завершения)'),
    ('process_time', 'Чистое время работы (от старта до завершения)'),
    ('waiting_time', 'Время ожидания (создание -> старт)'),
    ('review_time', 'Время проверки'),
]


STATUS_TO_PHASE = {
    'backlog': 'lead_time',
    'ready': 'waiting_time',
    'in_progress': 'process_time',
    'review': 'review_time',
    'done': 'lead_time',
    'cancelled': 'lead_time',
    'deleted': 'lead_time',
}


def logging_task_actions_handler(task_instance, action, **kwargs):
    """
    Универсальный обработчик действий с задачами.

    :param task_instance: Экземпляр задачи
    :param action: 'created' | 'updated' | 'deleted'
    :param kwargs:
        - old_instance: старая версия (для updated)
        - changed_fields: словарь изменений
        - user: кто совершил действие (если есть request)
    """

    try:
        with transaction.atomic():
            if action == 'created':
                # print(f"🆕 Задача создана: #{task_instance.id} - {task_instance.title}")
                # Здесь логика для новой задачи
                cycle_log = CycleTime.objects.get_or_create(task=task_instance)

                return cycle_log

            elif action == 'updated' and 'changed_fields' in kwargs:
                changes = kwargs['changed_fields'].get('status', {})

                if changes.get('from', None) == changes.get('to', None):
                    return
                # print(f"✏️  Задача обновлена: #{task_instance.id}")

                old_instance = kwargs.get('old_instance', None)
                if old_instance is None:
                    return

                if STATUS_TO_PHASE.get(task_instance.status, None) == 'lead_time':
                    if STATUS_TO_PHASE.get(old_instance.status, None) != 'lead_time':
                        updated_cycle_log = CycleTime.objects.filter(
                            task=old_instance,
                            phase=STATUS_TO_PHASE[old_instance.status],
                        ).first()
                        updated_cycle_log.end_time = timezone.now()
                        updated_cycle_log.save()

                    cycle_log = CycleTime.objects.filter(
                        task=task_instance,
                        phase=STATUS_TO_PHASE.get(task_instance.status, None)
                    ).first()
                    cycle_log.end_time = timezone.now()
                    cycle_log.save()
                    return cycle_log
                else:
                    if STATUS_TO_PHASE.get(old_instance.status, None) != 'lead_time':
                        updated_cycle_log = CycleTime.objects.filter(
                            task=old_instance,
                            phase=STATUS_TO_PHASE[old_instance.status],
                        ).first()
                        updated_cycle_log.end_time = timezone.now()
                        updated_cycle_log.save()

                    created_cycle_log = CycleTime.objects.create(
                        task=task_instance,
                        phase=STATUS_TO_PHASE[task_instance.status],
                    )
                    created_cycle_log.save()
                return created_cycle_log

            # Здесь можно добавить логику для:
            # 1. Отправки в Telegram/Slack
            # 2. Записи в Audit Log
            # 3. Обновления дэшбордов
            # 4. Инвалидации кеша
    except Exception as e:
        # try:
        #     return Profile.objects.create(user=user_instance)
        # except:
        raise e
