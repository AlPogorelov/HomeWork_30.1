from django.db import models

from courses.models import Course
from users.models import User


class Lesson(models.Model):

    lesson_name = models.CharField(max_length=200, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/preview/', verbose_name='Превью', blank=True, null=True, help_text="Превью для курса")
    description = models.TextField(verbose_name='Описание')
    video_url = models.URLField(verbose_name='Ссылка на видео')

    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, verbose_name='Курс')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор материала', blank=True, null=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
