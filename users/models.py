from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, verbose_name='Телефон', blank=True, null=True, help_text="Введите номер телефона")
    country = models.CharField(max_length=25, verbose_name='Страна', blank=True, null=True, help_text="Из какой вы страны")
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', blank=True, null=True, help_text="Загрузити свой аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payments(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_pay = models.DateTimeField(verbose_name='дата оплаты', blank=True, null=True)
    peid_materials = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE, verbose_name='оплаченный материал')
    payment_amount = models.FloatField(verbose_name='сумма платежа')
    payment_method = models.CharField(choices=[
        ('Cash', 'Cash'),
        ('Transfer', 'Transfer')
    ])
