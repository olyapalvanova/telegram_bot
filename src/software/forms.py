from telegram_django_bot import forms

from src.software.models import Software, License, Order


class SoftwareForm(forms.TelegramModelForm):
    class Meta:
        model = Software
        fields = ('name',)


class LicenseForm(forms.TelegramModelForm):
    class Meta:
        model = License
        fields = ('software', 'period_activity', 'status', 'price')


class OrderForm(forms.TelegramModelForm):
    class Meta:
        model = Order
        fields = ('user', 'license', 'price')
