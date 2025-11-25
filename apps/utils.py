"""Утилиты для инкапсуляции проверок в тестовых модулях"""

import io
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile


def is_django_field_empty(value):
    """Специально для Django полей модели"""
    # print(value.__dict__)
    if hasattr(value, '_state'):
        return value.id
    if hasattr(value, '_file'):  # FileField/ImageField
        return value.name is None
    return value is None or value == ''


def create_test_image(filename='test.jpg'):
    """Создаем реальное изображение в памяти"""
    image = Image.new('RGB', (100, 100), color='red')
    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)

    return SimpleUploadedFile(
        filename,
        image_io.getvalue(),
        content_type='image/jpeg'
    )
