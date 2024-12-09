from django.contrib import admin

from src.admin import ReadonlyModelAdmin

from .models import Software, License, Order


@admin.register(Software)
class SoftwareAdmin(ReadonlyModelAdmin):
    pass


@admin.register(License)
class LicenseAdmin(ReadonlyModelAdmin):
    list_display = ('id', 'software', 'status')
    list_filter = ('status',)


@admin.register(Order)
class OrderAdmin(ReadonlyModelAdmin):
    pass
