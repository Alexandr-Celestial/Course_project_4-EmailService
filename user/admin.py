from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdminModel(admin.ModelAdmin):
    list_display = list(f.name for f in User._meta.fields)
