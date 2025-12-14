from django.db import models

from apps.accounts.models import User
from apps.profiles.models import Profile
from apps.CONSTANTS import LANGUAGES


WORK_FORMATS = [
    ('office', 'офис'),
    ('hybrid', 'гибрид'),
    ('remote', 'удаленно'),
    ('any', 'любой')
]

PRIVACIES = [
    ('all', 'видно всем'),
    ('not_all', 'всем, кроме...'),
    ('nobody', 'никому')
]


class WorkExperience(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='experiences'
    )
    company = models.CharField(
        verbose_name='Компания работодатель',
        max_length=100, null=True, blank=True
    )
    indastry_desc = models.CharField(
        verbose_name='Краткое описание ниши работодателя',
        max_length=300, null=True, blank=True
    )
    start_year = models.SmallIntegerField(
        verbose_name='Год начала сотрудничества', null=True, blank=True
    )
    end_year = models.SmallIntegerField(
        verbose_name='Год окончания сотрудничества', null=True, blank=True
    )
    start_position = models.CharField(
        verbose_name='Стартовая должность', null=True, blank=True
    )
    final_position = models.CharField(
        verbose_name='Финальная должность', null=True, blank=True
    )
    is_current = models.BooleanField(default=False)
    privacy = models.CharField(
        verbose_name='Настройка видимости информации о работодателе',
        max_length=10, choices=PRIVACIES, default='all', blank=True
    )

    class Meta:
        verbose_name = 'Место работы или сотрудничества'
        verbose_name_plural = 'Места работы или сотрудничества'
        ordering = ['-start_year']

    def __str__(self):
        return f"{self.company} - {self.final_position or self.start_position}"


class WorkResult(models.Model):
    work_experience = models.ForeignKey(
        WorkExperience,
        on_delete=models.CASCADE,
        related_name='results'
    )
    result = models.CharField(
        verbose_name=(
            '[Действие] [Результат с цифрой] для [Контекст/Масштаб], '
            'используя [Метод/Инструмент], чтобы [Решаемая проблема]'
        ),
        max_length=500, null=True, blank=True
    )
    privacy = models.CharField(
        verbose_name='Настройка видимости рабочего результата',
        max_length=10, choices=PRIVACIES, default='all', blank=True
    )
    # action_and_impact = models.CharField(
    #     verbose_name=(
    #         'Идиома: '
    #         '"To drive" (вести, инициировать и контролировать). '
    #         '"To spearhead" (возглавлять, быть инициатором). '
    #         '"To champion" (отстаивать и продвигать).'
    #     ),
    #     max_length=100, null=True, blank=True
    # )
    # quantifiable_result = models.CharField(
    #     verbose_name=(
    #         'Идиома: '
    #         '"To deliver a X% increase in..." (обеспечить рост на X% в...). '
    #         '"To slash/cut costs by X%" (сократить затраты на X%). '
    #         '"To boost efficiency by [metric]" (повысить эффективность по показателю).'
    #     ),
    #     max_length=100, null=True, blank=True
    # )
    # scope_and_scale = models.CharField(
    #     verbose_name=(
    #         'Идиома: '
    #         '"Across a portfolio of..." (в рамках портфеля из...). '
    #         '"For a user base of X" (для аудитории в X пользователей). '
    #         '"Spanning X markets" (охватывая X рынков).'
    #     ),
    #     max_length=100, null=True, blank=True
    # )
    # methodology_or_tool = models.CharField(
    #     verbose_name=(
    #         'Идиома: '
    #         '"Leveraging [Tool/Method] to..." (используя [Инструмент/Метод] для...). '
    #         '"By implementing [Framework]" (путем внедрения [Подхода]). '
    #         '"Utilizing [Skill] to..." (применяя [Навык] для...).'
    #     ),
    #     max_length=100, null=True, blank=True
    # )
    # problem_solved = models.CharField(
    #     verbose_name=(
    #         'Идиома: '
    #         '"To address the challenge of..." (для решения задачи...). '
    #         '"To streamline the process of..." (для оптимизации процесса...). '
    #         '"To mitigate the risk of..." (для снижения риска...).'
    #     ),
    #     max_length=100, null=True, blank=True
    # )

    class Meta:
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'

    def __str__(self):
        return str(self.result)


# class TheHook(models.Model):
#     first_name = models.OneToOneField(
#         Profile, on_delete=models.CASCADE, related_name='the_hook'
#     )
#     last_name = models.OneToOneField(
#         Profile, on_delete=models.CASCADE, related_name='the_hook'
#     )
#     middle_name = models.CharField(max_length=50, null=True, blank=True)
#     role = models.CharField(max_length=50, null=True, blank=True)
#     title = models.CharField(max_length=50, null=True, blank=True)

#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE, related_name='hooks'
#     )

#     class Meta:
#         verbose_name = 'Ключевой идентификатор профессионализма'
#         verbose_name_plural = 'Ключевые идентификаторы профессионализма'

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'


# class TheLogistics(models.Model):
#     city = models.CharField(
#         verbose_name='Город нахождения',
#         max_length=100, null=True, blank=True
#     )
#     country = models.CharField(
#         verbose_name='Страна нахождения',
#         max_length=100, null=True, blank=True
#     )
#     relocation = models.CharField(
#         verbose_name='Готовность к релокации (куда)',
#         max_length=100, null=True, blank=True
#     )
#     work_format = models.CharField(
#         verbose_name='Предпочтительный формат работы',
#         choices=WORK_FORMATS, default='any', blank=True
#     )

#     hook = models.OneToOneField(
#         TheHook,
#         on_delete=models.CASCADE,
#         related_name='logistics'
#     )

#     class Meta:
#         verbose_name = 'Местонахождение пользователя'
#         verbose_name_plural = 'Местонахождения пользователей'

#     def __str__(self):
#         return f'{self.city} {self.country}'


# class TheCoreTimeLine(models.Model):
#     company = models.CharField(
#         verbose_name='Компания работодатель',
#         max_length=100, null=True, blank=True
#     )
#     indastry_desc = models.CharField(
#         verbose_name='Краткое описание ниши работодателя',
#         max_length=300, null=True, blank=True
#     )
#     start_year = models.SmallIntegerField(
#         verbose_name='Год начала сотрудничества', null=True, blank=True
#     )
#     end_year = models.SmallIntegerField(
#         verbose_name='Год окончания сотрудничества', null=True, blank=True
#     )
#     start_position = models.CharField(
#         verbose_name='Стартовая должность', null=True, blank=True
#     )
#     final_position = models.CharField(
#         verbose_name='Финальная должность', null=True, blank=True
#     )

#     work_results = models.ManyToManyField(
#         TheWorkResult,
#         verbose_name='Список результатов, достижений',
#         related_name='core_timeline'
#     )

#     hook = models.OneToOneField(
#         TheHook,
#         on_delete=models.CASCADE,
#         related_name='core_timeline'
#     )

#     class Meta:
#         verbose_name = 'Место работы или сотрудничества'
#         verbose_name_plural = 'Места работы или сотрудничества'

#     def __str__(self):
#         return f'{self.company}'


class SkillCluster(models.Model):
    """Модель для хранения уникальных кластеров навыков"""
    cluster_name = models.CharField(max_length=20, unique=True)
    order = models.PositiveSmallIntegerField(default=0, blank=True)
    # privacy = models.CharField(
    #     verbose_name='Настройка видимости кластера навыков',
    #     max_length=10, choices=PRIVACIES, default='all', blank=True
    # )

    class Meta:
        ordering = ['order', 'cluster_name']
        verbose_name = 'Кластер навыков'
        verbose_name_plural = 'Кластеры навыков'

    def __str__(self):
        return str(self.cluster_name)


class Skill(models.Model):
    """Модель для хранения уникальных навыков"""
    cluster = models.ForeignKey(
        SkillCluster,
        on_delete=models.CASCADE,
        default=1,
        related_name='skills'
    )
    skill_name = models.CharField(max_length=20, unique=True)
    # level = models.PositiveSmallIntegerField(
    #     choices=[(i, f"{i}/10") for i in range(1, 11)],
    #     null=True, blank=True
    # )
    privacy = models.CharField(
        verbose_name='Настройка видимости конкретного навыка',
        max_length=10, choices=PRIVACIES, default='all', blank=True
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='skills'
    )

    class Meta:
        unique_together = ['skill_name', 'profile']
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return str(self.skill_name)


# class TheHardSkillStack(models.Model):
#     cluster = models.ForeignKey(
#         TheCluster,
#         on_delete=models.CASCADE,
#         verbose_name='Кластер навыков',
#         related_name='hard_skill_stacks'
#     )
#     skills = models.ManyToManyField(
#         TheSkills,
#         verbose_name='Ключевые навыки',
#         related_name='hard_skills'
#     )

#     hook = models.OneToOneField(
#         TheHook,
#         on_delete=models.CASCADE,
#         related_name='skill_stack'
#     )

#     class Meta:
#         verbose_name = 'Кластер навыков'
#         verbose_name_plural = 'Кластеры навыков'

#     def __str__(self):
#         return str(self.cluster)


EDU_LEVEL = [
    ('not', 'не указано'),
    ('first_middle', '11 классов'),
    ('primary_voc_edu', 'Начальное профессиональное образование'),
    ('secondary_voc_edu', 'Среднее профессиональное образование'),
    ('higher_voc_edu', 'Высшее профессиональное образование')
]


def user_sertificate_path(instance, filename):
    """Персонализируется путь к сертификатам пользователя"""
    return f"sertificate/user_{instance.user.id}/{filename}"


class Sertificate(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    name = models.CharField(
        verbose_name='Полное название сертификата',
        max_length=300, null=True, blank=True
    )
    link_to_sertificate = models.URLField(
        verbose_name='Ссылка на сертификат', null=True, blank=True
    )
    image = models.ImageField(
        upload_to=user_sertificate_path, default='', blank=True
    )
    file = models.FileField(
        upload_to=user_sertificate_path, default='', blank=True
    )
    privacy = models.CharField(
        verbose_name='Настройка видимости сертификата',
        max_length=10, choices=PRIVACIES, default='all', blank=True
    )

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return str(self.name)


# class TheFoundation(models.Model):
#     edu_level = models.CharField(
#         verbose_name='Уровень государственного образования',
#         choices=EDU_LEVEL, default='not', blank=True
#     )
#     institution_name = models.CharField(
#         verbose_name='Наименование учебного заведения',
#         max_length=100, null=True, blank=True
#     )
#     graduation_year = models.SmallIntegerField(
#         verbose_name='Год окончания обучения', null=True, blank=True
#     )
#     additional_courses = models.BooleanField(
#         verbose_name='Наличие важных дополнительных курсов обучения',
#         default=False, blank=True
#     )
#     sertificates = models.ManyToManyField(
#         TheSertificate,
#         verbose_name='Список сертификатов',
#         related_name='foundations'
#     )

#     hook = models.OneToOneField(
#         TheHook,
#         on_delete=models.CASCADE,
#         related_name='foundation'
#     )

#     class Meta:
#         verbose_name = 'Сертификат'
#         verbose_name_plural = 'Сертификаты'

#     def __str__(self):
#         return str(self.edu_level)

class Language(models.Model):
    LANGUAGES = LANGUAGES
    LANGUAGE_LEVELS = [
        ('A1', 'Начальный (A1)'),
        ('A2', 'Элементарный (A2)'),
        ('B1', 'Средний (B1)'),
        ('B2', 'Выше среднего (B2)'),
        ('C1', 'Продвинутый (C1)'),
        ('C2', 'В совершенстве (C2)'),
        ('N', 'Родной'),
    ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='languages'
    )
    name = models.CharField(max_length=50,  choices=LANGUAGES)
    level = models.CharField(max_length=2, choices=LANGUAGE_LEVELS)
    privacy = models.CharField(
        verbose_name='Настройка видимости владения языком',
        max_length=10, choices=PRIVACIES, default='all', blank=True
    )

    class Meta:
        unique_together = ['profile', 'name']
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

    def __str__(self):
        return str(self.name)


class Summary(models.Model):
    """Модель для агрегации всех данных в резюме"""
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='summary'
    )
    professional_summary = models.TextField(
        verbose_name='Профессиональное резюме',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    privacy = models.CharField(
        verbose_name='Настройка видимости всего резюме целиком',
        max_length=10, choices=PRIVACIES, default='all', blank=True
    )

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'

    def __str__(self):
        return f"Резюме {self.profile}"
