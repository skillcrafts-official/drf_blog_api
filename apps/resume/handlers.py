from django.db import transaction

from apps.resume.models import WorkResult


def create_work_result_handler(work_experience):
    """
    Обработчик: Создает Profile для нового User
    """
    try:
        with transaction.atomic():
            work_result, _ = WorkResult.objects.get_or_create(
                work_experience=work_experience
            )
            return work_result

    except Exception as e:
        # try:
        #     return Profile.objects.create(user=user_instance)
        # except:
        raise e
