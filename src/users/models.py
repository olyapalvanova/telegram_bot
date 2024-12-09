from django.db import models

from telegram_django_bot.models import TelegramUser


class User(TelegramUser):
    is_bot_available = models.BooleanField(verbose_name='Разрешить пользователю использовать бота', default=False)
