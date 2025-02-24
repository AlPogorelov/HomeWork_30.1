import django.db.models.deletion

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True


        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_name', models.CharField(max_length=200, verbose_name='Название курса')),
                ('preview', models.ImageField(blank=True, help_text='Превью для курса', null=True, upload_to='course/preview/', verbose_name='Превью')),
                ('description', models.TextField(verbose_name='Описание')),
                ('video_url', models.URLField(verbose_name='Ссылка на видео')),

                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
            },
        ),
    ]
