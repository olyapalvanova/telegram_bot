from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'is_bot_available')
    list_filter = ('first_name', 'last_name', 'is_bot_available')
