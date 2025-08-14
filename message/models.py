from django.db import models

from user.models import User


class Message(models.Model):
    theme = models.CharField(max_length=150, verbose_name="Тема")
    body = models.TextField(max_length=200, verbose_name="Тело письма")
    owner = models.ForeignKey(
        User, verbose_name="Владелец письма", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
