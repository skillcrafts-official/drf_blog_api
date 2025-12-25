"""Файл с Django-моделями приложения Мои Дела"""
from django.db import models

from apps.accounts.models import User
from apps.profiles.models import Profile


PRIVACIES = [
    ('all', 'видно всем'),
    ('not_all', 'всем, кроме...'),
    ('no_one_except', 'никому, кроме'),
    ('nobody', 'никому')
]


class Task(models.Model):
    # --- Содержание (ваши текущие поля + статус) ---
    todo = models.CharField(null=True, blank=True)  # Краткое название/суть
    description = models.TextField(blank=True)       # Полное описание, контекст
    privacy = models.CharField(
        choices=PRIVACIES, max_length=20, default='nobody'
    )

    # --- Метаданные ПРОЦЕССА (ключ для KPI) ---
    STATUS_CHOICES = [
        ('backlog', 'Бэклог'),
        ('ready', 'Готово к работе'),
        ('in_progress', 'В работе'),
        ('review', 'На проверке'),
        ('done', 'Выполнено'),
        ('cancelled', 'Отменено'),
        ('deleted', 'Удалено'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='backlog'
    )  # Статус для расчета времени в каждом состоянии

    PRIORITY_CHOICES = [
        (1, 'Низкий'),
        (2, 'Средний'),
        (3, 'Высокий'),
        (4, 'Критичный'),
    ]
    priority = models.PositiveSmallIntegerField(
        choices=PRIORITY_CHOICES,
        default=2
    )  # Для анализа: "Какие приоритеты чаще срываются?"

    # --- Временные метки (ОСНОВА для Cycle Time) ---
    date_created = models.DateTimeField(auto_now_add=True)  # Создание запроса
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)  # Создание запроса
    date_ready = models.DateTimeField(null=True, blank=True)  # Попало в "Готово к работе"
    date_started = models.DateTimeField(null=True, blank=True)  # Фактический старт работы
    date_finished = models.DateTimeField(null=True, blank=True)  # Фактическое завершение работы

    # --- Ответственность и источники ---
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_tasks'
    )  # Кто отвечает за выполнение
    requester = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='requested_tasks'
    )  # Кто запросил (часто руководитель другого отдела)
    profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks'
    )  # Кто владелец задачи (в чьем профиле создана задача)
    # Будущее расширение, сейчас только задачи
    # project = models.ForeignKey(
    #     'Project',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True
    # )  # Группировка задач. Project — отдельная модель.

    # --- Плановые метрики (для сравнения "план vs факт") ---
    estimated_effort = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Оценка трудозатрат в часах'
    )  # Для точности оценок

    class Meta:
        ordering = ['-priority', '-date_updated', '-date_created']

    def __str__(self):
        return f"{self.pk}: {self.todo} ({self.get_status_display()})"


class CycleTime(models.Model):
    # Связь с задачей
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='cycle_logs'  # Более точное название
    )

    # --- КАКОЙ этап замеряем? ---
    PHASE_CHOICES = [
        ('lead_time', 'Полное время (от создания до завершения)'),
        ('process_time', 'Чистое время работы (от старта до завершения)'),
        ('waiting_time', 'Время ожидания (создание -> старт)'),
        ('review_time', 'Время проверки'),
    ]
    phase = models.CharField(
        max_length=20,
        choices=PHASE_CHOICES,
        default='lead_time',
    )

    # --- Данные для расчета ---
    start_time = models.DateTimeField(auto_now_add=True)  # Начало фазы
    end_time = models.DateTimeField(null=True, blank=True)    # Конец фазы
    duration_hours = models.FloatField(
        editable=False, null=True
    )  # Рассчитанное длительность в часах (можно вычислить автоматически)

    # --- Контекст для аналитики ---
    notes = models.TextField(
        null=True,
        blank=True,
        help_text='Что происходило на этом этапе? Блокировки, причины задержек'
    )

    class Meta:
        ordering = ['-end_time']

    def save(self, *args, **kwargs):
        # Автоматический расчет длительности при сохранении
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration_hours = delta.total_seconds() / 3600
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task.id} | {self.get_phase_display()}: {self.duration_hours:.1f} ч"


class AcceptanceCriteria(models.Model):
    """
    Модель описывающая критерии приёмки задачи.
    Каждый критерий является неотъемлемой частью задачи.
    """
    STATUS_CHOICES = [
        ('', '')
    ]
    criteria = models.TextField(null=True, blank=True)

    is_done = models.BooleanField(default=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='acceptance_criterias'
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.task.id} | {self.status}"
