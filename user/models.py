from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        null=False,
        verbose_name="Email",
        help_text="Введите адрес эл.почты",
    )
    avatar = models.ImageField(
        upload_to="avatar/", verbose_name="Аватар", null=True, blank=True
    )
    phone_number = models.CharField(max_length=30, verbose_name="Номер телефона", null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name="Страна", null=True, blank=True)
    token = models.CharField(max_length=100, null=True, blank=True, verbose_name='Токен')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_block_user", "Блокировка пользователя"),
            ('can_off_mailing', 'Отключение рассылки'),
        ]
