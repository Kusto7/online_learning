from django.conf import settings
from django.db import models

from users.models import NULLABLE, User


class Course(models.Model):
    """Модель онлайн курса"""

    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    link = models.URLField(verbose_name='ссылка', **NULLABLE, help_text='Ссылка на видео материалы')
    preview = models.ImageField(verbose_name='превью', **NULLABLE, help_text='Превью изображение для курса')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              help_text='Связано с моделью пользователя из приложение users.User')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """Модель онлайн урока"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', related_name='lesson', **NULLABLE,
                               help_text='Связано с моделью курса Course')
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(verbose_name='превью', **NULLABLE, help_text='Превью изображение для урока')
    link = models.URLField(verbose_name='ссылка', **NULLABLE, help_text='Ссылка на видео материалы')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              help_text='Связано с моделью пользователя из приложение users.User')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    """Модель платежа для курса или урока"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь',
                             help_text='Связано с моделью пользователя из приложение users.User')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE,
                               help_text='Для связи платежа с курсом Course')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE,
                               help_text='Для связи платежа с уроком Lesson')
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    method = models.CharField(max_length=50, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.amount}, {self.method}, — {self.user}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):

    """Модель подписки для курса"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, related_name='subscription',
                               verbose_name='Подписка на курс', help_text='Для связи курсом Course')
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Подписчик',
                                   **NULLABLE, help_text='Связано с моделью пользователя из приложение users.User')

    def __str__(self):
        return f'{self.course}:{self.subscriber}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
