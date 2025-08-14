from django.db import models

from user.models import User


class Recipient(models.Model):
    email = models.EmailField(verbose_name="Почта")
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    comments = models.TextField(verbose_name="Комментарий")
    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

