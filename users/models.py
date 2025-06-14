from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from courses.models import Course


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, verbose_name='Телефон', blank=True,
                             null=True, help_text="Введите номер телефона")
    country = models.CharField(max_length=25, verbose_name='Страна', blank=True,
                               null=True, help_text="Из какой вы страны")
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар',
                               blank=True, null=True, help_text="Загрузити свой аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):

        return self.email


class Payments(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_pay = models.DateTimeField(verbose_name='дата оплаты', blank=True, null=True)
    peid_materials = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE,
                                       verbose_name='оплаченный материал')
    payment_amount = models.PositiveIntegerField(verbose_name='сумма платежа')
    payment_method = models.CharField(choices=[
        ('Cash', 'Cash'),
        ('Transfer', 'Transfer')
    ])
    link_pay = models.URLField(max_length=400, blank=True, null=True, verbose_name='Ссылка на оплату')
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='id сессии')


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
