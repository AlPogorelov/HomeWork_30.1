from django.db import models


class Lesson(models.Model):

    lesson_name = models.CharField(max_length=200, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/preview/', verbose_name='Превью', blank=True, null=True, help_text="Превью для курса")
    description = models.TextField(verbose_name='Описание')
    video_url = models.URLField(verbose_name='Ссылка на видео')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
