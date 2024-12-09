from django.core.management.base import BaseCommand
from django.conf import settings

from telegram.ext import Updater
from telegram_django_bot.routing import RouterCallbackMessageCommandHandler
from telegram_django_bot.tg_dj_bot import TG_DJ_Bot


class Command(BaseCommand):
    help = 'Run telegram bot'

    def handle(self, *args, **options):
        updater = Updater(bot=TG_DJ_Bot(settings.TELEGRAM_TOKEN))

        updater.dispatcher.add_handler(RouterCallbackMessageCommandHandler())

        updater.start_polling()
        updater.idle()
