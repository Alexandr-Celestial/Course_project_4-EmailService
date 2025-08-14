from django.core.management import BaseCommand

from user.models import User


# Тестовые пользователи
class Command(BaseCommand):
    help = "Добавление тестового суперпользователя"

    def handle(self, *args, **options):
        test_users_data = [
            {
                "email": "admin@admin.com",
                "is_staff": True,
                "is_active": True,
                "is_superuser": True,
                "password": "1234",
            },
            {
                "email": "1@admin.com",
                "is_staff": False,
                "is_active": True,
                "is_superuser": False,
                "password": "1234",
            },
            {
                "email": "2@admin.com",
                "is_staff": False,
                "is_active": True,
                "is_superuser": False,
                "password": "1234",
            },
        ]
        for data_user in test_users_data:
            get_user = User.objects.filter(email=data_user["email"]).first()
            if not get_user:
                user: User = User.objects.create(
                    email=data_user["email"],
                    is_staff=data_user["is_staff"],
                    is_active=data_user["is_active"],
                    is_superuser=data_user["is_superuser"],
                )
                user.set_password(data_user["password"])
                user.save()
