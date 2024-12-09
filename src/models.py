from django.db import models


class CreatedAtModelMixin(models.Model):
    """Миксин для отслеживания даты создания объекта."""

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        abstract = True
