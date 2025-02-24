from django.db import models


from materials.models import Lesson


class Course(models.Model):

    course_name = models.CharField(max_length=200, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/preview/', verbose_name='Превью', blank=True, null=True, help_text="Превью для курса")
    description = models.TextField(verbose_name='Описание')

    lessons = models.ManyToManyField(Lesson)
    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


