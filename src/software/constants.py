from django.db import models


class LicenseStatus(models.TextChoices):
    ACTIVE = 'active', 'Активна'
    STOP = 'stop', 'Остановлена'
