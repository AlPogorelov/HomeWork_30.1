from django.db import models

from users.models import User


class Course(models.Model):

    course_name = models.CharField(max_length=200, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/preview/', verbose_name='Превью', blank=True, null=True, help_text="Превью для курса")
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор курса', blank=True, null=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
