from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Car

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение User в админке."""
    pass


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Отображение Car в админке."""
    pass
