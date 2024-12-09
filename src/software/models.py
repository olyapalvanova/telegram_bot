import uuid

from django.db import models

from src.models import CreatedAtModelMixin
from src.software.constants import LicenseStatus
from src.users.models import User


class Software(models.Model):
    """Программное обеспечение."""
    name = models.CharField(verbose_name='Имя', max_length=255)

    class Meta:
        verbose_name = 'Программное обеспечение'
        verbose_name_plural = 'Программные обеспечения'

    def __str__(self) -> str:
        return self.name


class License(CreatedAtModelMixin):
    """Лицензия."""
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='licenses')
    period_activity = models.PositiveIntegerField(verbose_name='Период активности в днях')
    status = models.CharField(verbose_name='Статус', choices=LicenseStatus.choices, default=LicenseStatus.ACTIVE)
    price = models.PositiveIntegerField(verbose_name='Цена')
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name = 'Лицензия'
        verbose_name_plural = 'Лицензии'

    def __str__(self) -> str:
        return f'{self.id}: {self.software}'


class Order(CreatedAtModelMixin):
    """Заказы."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    license = models.ForeignKey(License, on_delete=models.CASCADE, related_name='orders')
    price = models.PositiveIntegerField(verbose_name='Цена')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        unique_together = ('user', 'license')

    def __str__(self) -> str:
        return f'{self.user}: {self.license}'
