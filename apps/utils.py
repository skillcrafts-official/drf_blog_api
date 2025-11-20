"""Утилиты для инкапсуляции проверок в тестовых модулях"""


def is_django_field_empty(value):
    """Специально для Django полей модели"""
    if hasattr(value, 'name'):  # FileField/ImageField
        return value.name is None
    return value is None or value == ''
